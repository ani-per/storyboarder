# Storyboarder

**Storyboarder** is a visual set writing assistant. It consists of:

* Python scripts
  * `storyboarder.py`
    * The backend script that, given a visual answerline database, performs the generation of the visual answerline document and hybrid packets.
    * The hybrid packets are generated to interface with [`Oligodendrocytes`](https://github.com/hftf/oligodendrocytes). They have not been tested with [MODAQ](https://github.com/alopezlago/MODAQ), although the anticipation is that they will function properly.
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
2. Configure and run `config.py`.

## History

This project was created in March 2024 to handle setup for mirrors of [Untitled Film Set](https://hsquizbowl.org/forums/viewtopic.php?t=25325).
