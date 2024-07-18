from storyboarder import *  # noqa: F403

set_name = "Untitled Film Set"  # Name of the set/packet
db_dir = (
    Path.cwd() / "demo" / "untitled-film-set"
)  # Directory where the answerline document should be saved
db_path = (
    db_dir / f"{set_name.title().replace(' ', '-')}_Database.csv"
)  # Filepath of the answerline database CSV

storyboard(
    set_name,
    db_dir,
    db_path,
    hybrid=True,  # Is the set a hybrid visual-written tournament?
    raw_string="W",  # The suffix to identify the written packets. All written packets must end with this prefix for Storyboarder to identify them.
    src_dir=Path.home()
    / "Documents"
    / "AP"
    / "APMISC"
    / "quizbowl"
    / "storyboarder"
    / "demo"
    / "untitled-film-set"
    / "packets",  # The directory where the written packets are stored
    dest_dir=Path.home()
    / "Documents"
    / "AP"
    / "APMISC"
    / "quizbowl"
    / "oligo"
    / "tournaments"
    / "untitled-film-set"
    / "packets",  # The directory where the hybrid packets will be generated
    force_end=True,
    verbose=True,  # Print progress
)
