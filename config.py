from storyboarder import *

set_name = f"Untitled Film Set" # Name of the set/packet
db_dir = Path.cwd() / "demo" # Directory where the answerline document should be saved
db_path = (db_dir / f"{set_name.title().replace(' ', '-')}_Database.csv") # Filepath of the answerline database CSV

storyboard(
    set_name,
    db_dir,
    db_path,
    hybrid=True, # Is the set a hybrid visual-written tournament?
    raw_string="W", # The suffix to identify the written packets. All written packets must end with this prefix for Storyboarder to identify them.
    set_dir=Path.home() / "Documents" / "quizbowl" / "oligo" / "tournaments" / "untitled-film-set" / "packets", # The directory where the written packets are stored (and where the hybrid packets will be generated)
    verbose=True # Print progress
)
