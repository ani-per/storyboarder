from storyboarder import *  # noqa: F403

set_name = "Untitled Film Set"  # Name of the set/packet
db_dir = (
    Path.cwd() / "demo" / "Untitled-Film-Set"
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
    src_dir=db_dir / "packets",  # The directory where the written packets are stored
    # dest_dir=db_dir / "packets",  # The directory where the hybrid packets will be generated, if different from `src_dir`
    force_end=True,  # Should the written equivalent of the visual slides end with the penultimate number for MODAQ use, or should they end with the final number? Defaults to True.
    verbose=True,  # Print progress
)
