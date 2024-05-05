def changelog(version: str):
	if version == "latest":
		version = "2.35.0"
	with open("resources/changelog.txt", "r") as f:
		lines = f.readlines()
		try:
			verIndex = lines.index(f"Version {version}\n")
		except ValueError:
			return "No changelog found"
		changelog = ""
		for line in lines[verIndex::]:
			if line == "End of changelog\n":
				break
			changelog += line
		return changelog
