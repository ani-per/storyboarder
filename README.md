# Storyboarder

**Storyboarder** is an assistant for writing visual quizbowl sets, created by Ani Perumalla in 2024. Storyboarder can handle sets/packets that are **fully visual** (e.g. [Eyes That Do Not See](https://collegiate.quizbowlpackets.com/1906/)) or **hybrid written + visual** (e.g. [Untitled Film Set](https://collegiate.quizbowlpackets.com/3197/)). The primary purpose is to assist in production of film sets, but Storyboarder can be used for visual packets that draw from any combination of media (film, television, online videos, art, photography, literature, etc.).

It automatically creates:

* A roughly-formatted visual answerline document that contains both answerlines and slide-by-slide information for each visual question.
* If `hybrid` is configured, a set of hybrid packets that contain any combination of written and visual questions, for convenient use by moderators using [Oligodendrocytes](https://github.com/hftf/oligodendrocytes) or [MODAQ](https://github.com/alopezlago/MODAQ).

> [!IMPORTANT]
> The hybrid packet generation is compatible with both [Oligodendrocytes](https://github.com/hftf/oligodendrocytes) and [MODAQ](https://github.com/alopezlago/MODAQ) (which also uses [YAPP](https://github.com/alopezlago/YetAnotherPacketParser)). The pipeline to interface with MODAQ has been thoroughly tested for [Untitled Film Set](https://collegiate.quizbowlpackets.com/3197/).

## Requirements

* [Python(3)](https://www.python.org/downloads/)
* [A properly-configured visual answerline database CSV](demo/Untitled-Film-Set_Database.csv)
* If `hybrid` is configured, [a set of packets as Word documents](demo/packets/) that contain the questions for the written portion of a hybrid tournament

## Contents

* [Google Drive folder](https://drive.google.com/drive/folders/1uJXE8UJXxA2VepXUR7n4mBuHC4J9txpS?usp=sharing)
  * [Google Slides template for standardized, color-coded visual packets](https://docs.google.com/presentation/d/1CbMiGaGSL4gyph7laR1obxKAvC_3cW-cDHVXUdTcqBk/edit?usp=sharing) [^1]
  * [A visual answerline database template](https://docs.google.com/spreadsheets/d/1r6tFbcZvPioG1RqSINoclno7yGYWZSv-Ygo0qBbxQq0/edit?usp=sharing) [^2] (which should be exported as a CSV once configured)
* Python scripts
  * [`storyboarder.py`](storyboarder.py)
    * The backend script that, given a properly-configured visual answerline database CSV, performs the generation of the visual answerline document and hybrid packets.
  * [`config.py`](config.py)
    * The front-facing script that configures the set metadata and how to perform the creation.

## Usage

1. Install, e.g. using [`pip`](https://pip.pypa.io/en/stable/):
   * [`pandas`](https://pandas.pydata.org/)
   * [`python-docx`](https://github.com/python-openxml/python-docx)
   * [`haggis`](https://gitlab.com/madphysicist/haggis)
   * [`tmdbv3api`](https://github.com/AnthonyBloomer/tmdbv3api)
2. Setup the visual answerline database using the template as an example.
   * Each visual question comprised of $n$ slides corresponds to $n$ rows.
   * Each row per question, including the first, must contain the other metadata about the source of the respective slide (`Packet`, `Number`, `Source` and `Value`).
   * The first row for each question is special in that it must *also* contain the necessary metadata about the question (`Answerline` and `Answerline_Type` [^3]).
   * Make sure to use the correct `Answerline_Type` based on the answerline. The following `Answerline_Types` are recognized by Storyboarder:
     * `Film`
     * `Creator`
     * `Director`
     * `Figure`
     * `Crew`
     * `Location`
     * `Surname`
     * `Misc`
   * Optional columns are `Source_Type`, `Source_Year`, and `Creator`.
     * Storyboarder automatically populates the information regarding film directors using the `tmdbv3api` utility to search [TMDB](https://www.themoviedb.org/movie).
     * To help the automatic detection, you may provide the film's release year in the `Source_Year` column for the corresponding row.
     * To override the automatic results for a given `Source`, you can explicitly assign its `Creator` in the corresponding cell.
     * The default `Source_Type` per source is assumed to be `Film`, so unless the `Source` is not a film, you may leave the corresponding cell empty.
     * To reference a music video, video game, or essay in a slide rather than a film for a given `Source`, change the `Source_Type`. Specifically for the `Music Video` type, add quotation marks around the `Source` value.
3. Configure the parameters in `config.py` and run `config.py`.
4. You should now have:
   * A roughly-formatted visual answerline document that contains both answerlines and slide-by-slide information for each visual question.
   * (If configured) a set of hybrid packets that contain both written and visual questions for convenient use by moderators using [MODAQ](https://github.com/alopezlago/MODAQ) or [Oligodendrocytes](https://github.com/hftf/oligodendrocytes).

## Example

See the `Untitled-Film-Set` directory of this repository for a set of example packets generated using the database template and scripts for [2024 Untitled Film Set](https://collegiate.quizbowlpackets.com/3197/).

## Notes

> [!WARNING]
> Make sure you close all Storyboarder-generated files (hybrid packets, visual answerlines spreadsheet) before running `config.py`, since `python-docx` cannot rewrite any files that are currently open and will hence throw an error.

> [!IMPORTANT]
> Storyboarder can handle fully-visual tournaments. Just configure `hybrid = True` and create a set of empty packet files in `set_dir` to act as the "written" files.

> [!WARNING]
> Storyboarder performs a first run of formatting on each answerline. However, once Storyboarder has been run, you should go through each visual answerline and format it as per [style guides](https://minkowski.space/quizbowl/manuals/style/), as there will likely be errors. Hence, it is recommended (but not required) to make sure that the answerlines for the written portion of a hybrid set are verified and proofreaded before running Storyboarder.

## History

`2024-03-24`: This project was created to handle setup for mirrors of [Untitled Film Set](https://hsquizbowl.org/forums/viewtopic.php?t=25325) (privately, since the set was used for testing and was not yet played at that time).

`2024-09-27`: The scripts were updated to automatically populate answerlines with information about film directors, using the [`tmdbv3api` package](https://github.com/AnthonyBloomer/tmdbv3api).

## Feedback

Please [create an issue](https://github.com/ani-per/storyboarder/issues/new). [Pull requests](https://github.com/ani-per/storyboarder/compare) are welcomed!

[^1]: The slide template uses the [Wong](https://www.nature.com/articles/nmeth.1618) [colorblind-friendly palette](https://davidmathlogic.com/colorblind/).
[^2]: Note that this template assumes that each visual question is comprised of exactly 8 slides. However, the scripts can handle any question length.
[^3]: All other columns (`Difficulty`, `Continent`, etc.) are just for benefit of the writers and are not actually used in the processing.
