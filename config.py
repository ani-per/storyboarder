from storyboarder import *

set_name = f"Untitled Film Set" # Name of the set/packet
db_dir = Path.cwd() / "demo" # Directory where the answerline document should be saved
db_path = (db_dir / f"{set_name.title().replace(' ', '-')}_Database.csv") # Filepath of the answerline database CSV

storyboard(
    set_name,
    db_dir,
    db_path,
    hybrid=True, # Is the set a hybrid visual-written tournament?
    raw_string="W", # The suffix to identify the written packets
    set_dir=Path.home() / "Documents" / "quizbowl" / "oligo" / "tournaments" / "untitled-film-set" / "packets", # The directory where the written packets are stored (and where the hybrid packets will be generated)
    split_docs=False, # Should the answerline documents be split?
    tags=True, # Should the hybrid packets have author tags for the visual questions?
    verbose=True # Print progress
)
