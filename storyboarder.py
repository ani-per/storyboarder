import itertools as it  # Readable nested for loops
from pathlib import Path  # Filepaths
import typing # Argument / output type checking
import pandas as pd # DataFrames
import docx as docx # Word documents - https://github.com/python-openxml/python-docx
from haggis.files.docx import list_number # Misc Word document utils - https://gitlab.com/madphysicist/haggis
from re import sub, search, findall

from subprocess import call
from platform import system
from os import startfile

# https://stackoverflow.com/a/40319071
def _copy(self, target):
    from shutil import copy as sh_copy
    assert self.is_file()
    sh_copy(str(self), str(target))

Path.copy = _copy

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
            if i == (n_main_names - 1):
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

    if len(ans_split) > 1:
        # Style the alt answerlines if they exist
        alt_ans = search(r'\[(.*?)\]', "[" + ans_split[1]).group(1).split("; ")
        n_alt_ans = len(alt_ans)
        alt_ans_runs = n_alt_ans*[None]
        for i in range(n_alt_ans):
            for directive in ["or ", "accept ", "prompt on ", "reject "]:
                if alt_ans[i].startswith(directive):
                    if i == 0:
                        ans_par.add_run(" [")
                    ans_par.add_run(directive)
                    if ans_type in ["Director", "Crew", "Figure"]:
                        alt_names = alt_ans[i].split(directive)[-1].split(" ")
                        n_alt_names = len(alt_names)
                        alt_name_runs = n_alt_names*[None]
                        for j in range(n_alt_names):
                            alt_name_runs[j] = ans_par.add_run(alt_names[j])
                            if j == (n_alt_names - 1):
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
                    if i == (n_alt_ans - 1):
                        ans_par.add_run("]")
                    else:
                        ans_par.add_run("; ")

def style_doc(tmpl):
    # tmpl.styles["Heading 1"].font = ""
    pass

# Set parameters

verbose = True

set_name = f"Untitled Film Set"
set_slug = set_name.title().replace(" ", "-")

db_dir = Path.cwd() / "demo"
ans_db = pd.read_csv((db_dir / f"{set_slug}_Database.csv")).convert_dtypes() # Source: Database CSV

# Is the set a hybrid visual-written tournament?
hybrid = True
raw_string = "W" # "_raw"
set_dir = Path.home() / "Documents" / "quizbowl" / "oligo" / "tournaments" / "untitled-film-set" / "packets"

split_docs = False # Should the answerline documents be split?

# Begin processing

packet_names = list(ans_db["Packet"].unique())
n_packet = len(packet_names)

templates = n_packet*[None]
documents = n_packet*[None]
packets = n_packet*[None]
answers = n_packet*[ans_db["Number"].max()*[None]]
slides = n_packet*[ans_db["Number"].max()*[[None]]]

for i in range(n_packet):
    if split_docs or (not split_docs and (i == 0)):
        templates[i] = docx.Document()
        if split_docs:
            documents[i] = (db_dir / f"{set_slug}_Answers-raw_{packet_names[i].zfill(2)}.docx")
        elif not split_docs and (i == 0):
            documents[i] = (db_dir / f"{set_slug}_Answers-raw.docx")
    elif (not split_docs) and (i > 0):
        templates[i] = templates[0]
        documents[i] = documents[0]

# Use curly quotes
for col in ["Answerline", "Source", "Director", "Notes"]:
    ans_db[col] = ans_db[col].apply(lambda s: make_curly(s) if pd.notnull(s) else s)

# Prepare the hybrid packet generation, if configured
make_hybrid = True
if hybrid and set_dir.exists():
    written_packets = sorted(set_dir.glob(f"**/*{raw_string}.docx"))
    if len(list(written_packets)) == n_packet:
        make_hybrid = True
        hybrid_packets = n_packet*[None]
        hybrid_answers = n_packet*[ans_db["Number"].max()*[None]]
    else:
        print("Number of placeholder packets doesn't match the number of written packets.")

for i in range(n_packet): # Loop over packets
    style_doc(templates[i])
    if (split_docs) or ((not split_docs) and (i == 0)):
        templates[i].add_heading(f"{set_name} - Visual Answerlines", level=0)
    elif (not split_docs) and (i > 0):
        templates[i].add_page_break()
    packet_header = f"Packet {packet_names[i]}"
    packets[i] = templates[i].add_heading(packet_header, level=1)

    if verbose:
        print(packet_header)

    # Filter the database to the current packet
    packet_db = ans_db[ans_db["Packet"] == packet_names[i]]

    # If hybrid, make the current hybrid packet by appending to the corresponding written packet
    if make_hybrid:
        hybrid_packets[i] = written_packets[i].parent / f"{set_slug}_{packet_names[i].zfill(2)}.docx"
        if hybrid_packets[i].exists():
            hybrid_packets[i].unlink()
        Path.copy(written_packets[i], hybrid_packets[i])
        hybrid_docx = docx.Document(hybrid_packets[i])
        # Calculate the number of already-written questions in the packet
        # This compiles all the numbers in the document that are succeeded by a period, then takes the maximum
        # https://stackoverflow.com/questions/952914/how-do-i-make-a-flat-list-out-of-a-list-of-lists#comment123215183_952952
        n_written = max([int(s) for s in [leaf for tree in [findall("(^\d+)\.+", s) for s in [p.text for p in hybrid_docx.paragraphs]] for leaf in tree if leaf]])

    for j in range(packet_db["Number"].max()): # Loop over questions
        # Filter the database to the current question
        q_db = packet_db[packet_db["Number"] == (j + 1)]
        n_slide = q_db.shape[0]

        # Only process if the answerline is not empty
        if pd.notnull(q_db.iloc[0]["Answerline"]):
            # Write the answerline
            answers[i][j] = templates[i].add_paragraph("", style="List Number")
            write_answerline(answers[i][j], q_db.iloc[0]["Answerline"], q_db.iloc[0]["Type"])

            if verbose:
                print(f"{j + 1}: " + q_db.iloc[0]["Answerline"])

            # If hybrid, make the placeholder question
            if make_hybrid:
                hybrid_docx.add_paragraph("")
                slide_q = hybrid_docx.add_paragraph(f"{j + n_written + 1}. ")
                slide_runs = n_slide*[None]
                for k in range(n_slide): # Loop over slides
                    slide_runs[k] = slide_q.add_run(f"{k + 1}" + f" "*(k < (n_slide - 1)))
                    if k < (n_slide - 1):
                        if q_db.iloc[k]["Value"] == 20:
                            slide_runs[k].bold = True
                            slide_runs[k].underline = True
                            if q_db.iloc[k + 1]["Value"] < 20:
                                superpower_mark = slide_q.add_run(f"(+)")
                                superpower_mark.bold = True
                                superpower_mark.underline = True
                                slide_q.add_run(f" ")
                        elif q_db.iloc[k]["Value"] == 15:
                            slide_runs[k].bold = True
                            if q_db.iloc[k + 1]["Value"] < 15:
                                power_mark = slide_q.add_run(f"(*)")
                                power_mark.bold = True
                                slide_q.add_run(f" ")

                hybrid_answers[i][j] = hybrid_docx.add_paragraph("ANSWER: ")
                write_answerline(hybrid_answers[i][j], q_db.iloc[0]["Answerline"], q_db.iloc[0]["Type"])

            if q_db.iloc[0]["Type"] == "Film": # If it's a film, write the director in the answerline
                dir_raw = f" (dir. {q_db.iloc[0]['Director']})"
                answers[i][j].add_run(dir_raw)
                if (make_hybrid):
                    hybrid_answers[i][j].add_run(dir_raw)
            else: # Prepare the slide annotations, if it's not a film
                slides[i][j] = n_slide*[None]
                for k in range(n_slide): # Loop over slides
                    # Add an annotation if there's a source listed for the current slide
                    if pd.isna(q_db.iloc[k]["Source"]):
                        src_raw = ""
                    else:
                        src_raw = q_db.iloc[k]["Source"]

                    # Write the slide annotation
                    slides[i][j][k] = templates[i].add_paragraph("", style="List Number 2")
                    src_run = slides[i][j][k].add_run(src_raw)
                    if (len(src_raw) > 0) and not (q_db.iloc[k]["Source"].startswith(("\'", "\"", "‘", "“"))): # Don't italicize if title's in quotes (e.g. music video)
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
                    if k == 0:
                        list_number(templates[i], slides[i][j][k], prev=None, level=0)
                    else:
                        list_number(templates[i], slides[i][j][k], prev=slides[i][j][k - 1])

            # If there are notes, write them
            if not pd.isna(q_db.iloc[0]["Notes"]):
                notes_raw = f" ({q_db.iloc[0]['Notes']})"
                answers[i][j].add_run(notes_raw)

            if j == 0:
                list_number(templates[i], answers[i][j], prev=None, level=0)
            else:
                list_number(templates[i], answers[i][j], prev=answers[i][j - 1])

    if make_hybrid:
        hybrid_docx.save(hybrid_packets[i])
    # Write the document
    templates[i].save(documents[i])

if not split_docs:
    # https://stackoverflow.com/a/435669
    if system() == "Darwin": # MacOS
        call(("open", documents[0]))
    elif system() == "Windows": # Windows
        startfile(documents[0])
    else: # Linux variants
        call(("xdg-open", documents[0]))
