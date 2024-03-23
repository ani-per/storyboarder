# Storyboarder

**Storyboarder** is a visual set writing assistant.

It automatically creates:

* A roughly-formatted visual answerline document that contains both answerlines and slide-by-slide information for each visual question.
* If `hybrid` is configured, a set of hybrid packets that contain both written and visual questions for convenient use by moderators using [Oligodendrocytes](https://github.com/hftf/oligodendrocytes).

It requires:

* Python3
* A visual answerline database CSV
* If `hybrid` is configured, a set of packets as Word documents that contain the questions for the written portion of a hybrid tournament

It consists of:

* Python scripts
  * `storyboarder.py`
    * The backend script that, given a visual answerline database, performs the generation of the visual answerline document and hybrid packets.
  * `config.py`
    * The front-facing script that configures the set metadata and how to perform the creation.
* Google Drive folder
  * Google Slides templates for standardized, color-coded visual packets
  * A visual answerline database template

## Usage

1. Install, preferably using [`pip`](https://pip.pypa.io/en/stable/):
   * [`pandas`](https://pandas.pydata.org/)
   * [`python-docx`](https://github.com/python-openxml/python-docx)
   * [`haggis`](https://gitlab.com/madphysicist/haggis)
2. Setup the visual answerline database using the template as an example.
   * Each visual question comprised of $n$ slides corresponds to $n$ rows.
   * The first row is special in that it should contain the necessary metadata about the question (`Answerline` and `Type` [^1]).
   * Each row, including the first, should contain the other metadata about the source of the respective slide (`Source`, `Director`, `Value`).
   * Make sure to use the correct `Type` based on the answerline. The following `Types` are recognized by Storyboarder:
     * `Film`
     * `Director`
     * `Figure`
     * `Crew`
   * To reference a music video in a slide rather than a film, put the name of the music video in quotation marks in the corresponding `Source` cell for that slide.
3. Configure and run `config.py`.
4. You should now have:
   * A roughly-formatted visual answerline document that contains both answerlines and slide-by-slide information for each visual question.
   * If configured, a set of hybrid packets that contain both written and visual questions for convenient use by moderators using [Oligodendrocytes](https://github.com/hftf/oligodendrocytes).

> [!IMPORTANT]
> The hybrid packets are generated to interface with [Oligodendrocytes](https://github.com/hftf/oligodendrocytes). They have not been tested with [MODAQ](https://github.com/alopezlago/MODAQ), although the anticipation is that they will function properly.

> [!WARNING]
> Storyboarder performs a first run of formatting on each answerline. However, once Storyboarder has been run, you should go through each visual answerline and format it as per [style guides](https://minkowski.space/quizbowl/manuals/style/), as there will likely be errors. Hence, it is recommended (but not required) to make sure that the answerlines for the written portion of a hybrid set are verified and proofreaded before running Storyboarder.

## History

`2024-03-24`: This project was created to handle setup for mirrors of [Untitled Film Set](https://hsquizbowl.org/forums/viewtopic.php?t=25325) (privately, since the set was used for testing and was not yet played at that time).

## Feedback

Please [create an issue](https://github.com/ani-per/storyboarder/issues/new). [Pull requests](https://github.com/ani-per/storyboarder/compare) are welcomed!

[^1]: All other columns (`Difficulty`, `Continent`, etc.) are just for benefit of the writers and are not actually used in the processing.
