import itertools as it  # Readable nested for loops
from pathlib import Path  # Filepaths
import typing  # Argument / output type checking
import pandas as pd # DataFrames
import docx as docx # Word documents - https://github.com/python-openxml/python-docx
from haggis.files.docx import list_number # Misc Word document utils - https://gitlab.com/madphysicist/haggis
from re import sub, search

from subprocess import call
from platform import system
from os import startfile

# https://stackoverflow.com/a/38234962
def make_curly(str):
    return sub(r"(\s|^)\'(.*?)\'(\s|$)", r"\1‘\2’\3", sub(r"\"(.*?)\"", r"“\1”", str)).replace("\'", "’")

def write_answerline(ans_par, ans_raw, ans_type):
    ans_split = ans_raw.split(" [")
    main_ans = ans_split[0]

    # Style the main answerline first
    if ans_type in ["Director", "Crew", "Figure"]:
        main_names = main_ans.split(" ")
        n_main_names = len(main_names)
        main_runs = n_main_names*[None]
        for i in range(n_main_names):
            main_runs[i] = ans_par.add_run(main_names[i])
            if (i == (n_main_names - 1)):
                main_runs[i].bold = True
                main_runs[i].underline = True
            else:
                ans_par.add_run(" ")
    else:
        main_run = ans_par.add_run(main_ans)
        main_run.bold = True
        main_run.underline = True
    if ans_type == "Film":
        main_run.italic = True

    if (len(ans_split) > 1):
        # Style the alt answerlines if they exist
        alt_ans = search(r'\[(.*?)\]', "[" + ans_split[1]).group(1).split("; ")
        n_alt_ans = len(alt_ans)
        alt_ans_runs = n_alt_ans*[None]
        for i in range(n_alt_ans):
            for directive in ["or ", "accept ", "prompt on ", "reject "]:
                if alt_ans[i].startswith(directive):
                    if (i == 0):
                        ans_par.add_run(" [")
                    ans_par.add_run(directive)
                    if ans_type in ["Director", "Crew", "Figure"]:
                        alt_names = alt_ans[i].split(directive)[-1].split(" ")
                        n_alt_names = len(alt_names)
                        alt_name_runs = n_alt_names*[None]
                        for j in range(n_alt_names):
                            alt_name_runs[j] = ans_par.add_run(alt_names[j])
                            if (j == (n_alt_names - 1)):
                                if not directive.startswith("reject"):
                                    alt_name_runs[j].underline = True
                                    if not directive.startswith("prompt"):
                                        alt_name_runs[j].bold = True
                                    if ans_type == "Film":
                                        alt_name_runs[j].italic = True
                            else:
                                ans_par.add_run(" ")
                    else:
                        alt_ans_runs[i] = ans_par.add_run(alt_ans[i].split(directive)[-1])
                        if not directive.startswith("reject"):
                            alt_ans_runs[i].underline = True
                            if not directive.startswith("prompt"):
                                alt_ans_runs[i].bold = True
                            if ans_type == "Film":
                                alt_ans_runs[i].italic = True
                    if (i == (n_alt_ans - 1)):
                        ans_par.add_run("]")
                    else:
                        ans_par.add_run("; ")

def style_doc(tmpl):
    # tmpl.styles['Heading 1'].font = ""
    pass

set_dir = Path.cwd() / "demo"
set_name = f"Untitled Film Set"
set_slug = set_name.title().replace(" ", "-")
ans_db = pd.read_csv((set_dir / "Untitled-Film-Set_Database.csv")).convert_dtypes() # Source: Database CSV

split_docs = False # Should the answerline documents be split?
if split_docs: # TODO
    pass
else:
    ans_tmpl = docx.Document()
    ans_docx = (set_dir / f"{set_slug}_Answers-raw.docx") # Output: ans_raw document (docx)
    ans_md = (set_dir / f"{set_slug}_Answers-raw.md") # Output: ans_raw document (md)
    ans_txt = (set_dir / f"{set_slug}_Answers-raw.txt") # Output: ans_raw document (md)

n_pack = ans_db["Packet"].max()
n_q = ans_db["Number"].max()
n_q = ans_db["Number"].max()

packets = n_pack*[None]
answers = n_pack*[n_q*[None]]
slides = n_pack*[n_q*[[None]]]

style_doc(ans_tmpl)

ans_tmpl.add_heading(f"{set_name} - Visual Answerlines", level=0)
for i in range(n_pack): # Loop over packets
    if (i > 0):
        ans_tmpl.add_page_break()
    pack_raw = f"Packet {i + 1}"
    packets[i] = ans_tmpl.add_heading(pack_raw, level=1)
    for j in range(n_q): # Loop over questions
        # Filter just the current question
        q_db = ans_db[(ans_db["Packet"] == (i + 1)) & (ans_db["Number"] == (j + 1))]

        # Write the answerline
        answers[i][j] = ans_tmpl.add_paragraph("", style="List Number")
        write_answerline(answers[i][j], make_curly(q_db.iloc[0]["Answerline"]), q_db.iloc[0]["Type"])
        if q_db.iloc[0]["Type"] == "Film": # If it's a film, we can just list the director here
            dir_raw = f" (dir. {q_db.iloc[0]['Director']})"
            answers[i][j].add_run(dir_raw)
        if not pd.isna(q_db.iloc[0]["Notes"]):
            notes_raw = f" ({q_db.iloc[0]['Notes']})"
            answers[i][j].add_run(notes_raw)
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
                if (q_db.iloc[0]["Type"] != "Director") or (q_db.iloc[0]["Type"] == "Director" and not pd.isna(q_db.iloc[k]["Director"])):
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
