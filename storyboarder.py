import itertools as it  # Readable nested for loops
from pathlib import Path  # Filepaths
import typing  # Argument / output type checking
import pandas as pd # DataFrames
import docx as docx # Word documents
from haggis.files.docx import list_number # Misc Word document utils
from re import sub

from subprocess import call
from platform import system
from os import startfile

# https://stackoverflow.com/a/38234962
def make_curly(str):
    return sub(r"(\s|^)\'(.*?)\'(\s|$)", r"\1‘\2’\3", sub(r"\"(.*?)\"", r"“\1”", str))

set_dir = Path.cwd() / "demo"
set_name = f"Untitled Film Set"
set_slug = set_name.title().replace(" ", "-")
ans_db = pd.read_csv((set_dir / "Untitled-Film-Set_Database.csv")).convert_dtypes() # Source: Database CSV

split_docs = False # Should the answerline documents be split?
if split_docs: # TODO
    pass
else:
    ans_tmpl = docx.Document()
    ans_docx = (set_dir / f"{set_slug}_Answers.docx") # Output: ans_raw document (docx)
    ans_md = (set_dir / f"{set_slug}_Answers.md") # Output: ans_raw document (md)
    ans_txt = (set_dir / f"{set_slug}_Answers.txt") # Output: ans_raw document (md)

n_pack = ans_db["Packet"].max()
n_q = ans_db["Number"].max()
n_q = ans_db["Number"].max()

packets = n_pack*[None]
answers = n_pack*[n_q*[None]]
slides = n_pack*[n_q*[[None]]]

ans_tmpl.add_heading(f"{set_name} - Visual Answerlines", level=0)
for i in range(n_pack): # Loop over packets
    if (i > 0):
        ans_tmpl.add_page_break()
    pack_raw = f"Packet {i + 1}"
    packets[i] = ans_tmpl.add_heading(pack_raw, level=1)
    for j in range(n_q): # Loop over questions
        # Filter just the current question
        q_db = ans_db[(ans_db["Packet"] == (i + 1)) & (ans_db["Number"] == (j + 1))]

        # Prepare the answerline
        ans_raw = make_curly(q_db.iloc[0]["Answerline"])
        if q_db.iloc[0]["Type"] == "Film": # If it's a film, we can just list the director here
            ans_raw += f" (dir. {q_db.iloc[0]['Director']})"
        # Write the answerline
        answers[i][j] = ans_tmpl.add_paragraph(ans_raw, style="List Number")
        if (j == 0):
            list_number(ans_tmpl, answers[i][j], prev=None, level=0)
        else:
            list_number(ans_tmpl, answers[i][j], prev=answers[i][j - 1])

        # Prepare the slide annotations, if it's not a film
        if q_db.iloc[0]["Type"] != "Film":
            n_slide = q_db.shape[0]
            slides[i][j] = n_slide*[None]
            for k in range(n_slide): # Loop over slides
                # Add an annotation if there's a source listed for the current slide
                if pd.isna(q_db.iloc[k]["Source"]):
                    src_raw = ""
                else:
                    src_raw = make_curly(q_db.iloc[k]["Source"])

                # Write the slide annotation
                slides[i][j][k] = ans_tmpl.add_paragraph("", style="List Number 2")
                src_run = slides[i][j][k].add_run(src_raw)
                if (len(src_raw) > 0) and not (q_db.iloc[k]["Source"].startswith("\"")): # Don't italicize if title's in quotes (e.g. music video)
                    src_run.italic = True

                # If the question's not a Director, add the director credit for the source of the current slide
                if q_db.iloc[0]["Type"] != "Director":
                    if (k > 0) and (pd.isna(q_db.iloc[k]["Director"])) and not (pd.isna(q_db.iloc[0]["Director"])):
                        dir_raw = f" (dir. {q_db.iloc[0]['Director']})"
                    elif not (pd.isna(q_db.iloc[k]["Director"])):
                        dir_raw = f" (dir. {q_db.iloc[k]['Director']})"
                    else:
                        dir_raw = ""
                    slides[i][j][k].add_run(dir_raw)

                # Format the annotation as a list element
                if (k == 0):
                    list_number(ans_tmpl, slides[i][j][k], prev=None, level=0)
                else:
                    list_number(ans_tmpl, slides[i][j][k], prev=slides[i][j][k - 1])

# Write the document
ans_tmpl.save(ans_docx)

# https://stackoverflow.com/a/435669
if system() == "Darwin": # MacOS
    call(("open", ans_docx))
elif system() == 'Windows': # Windows
    startfile(ans_docx)
else: # Linux variants
    call(("xdg-open", ans_docx))
