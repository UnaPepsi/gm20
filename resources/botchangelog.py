async def changelog(version: str) -> str:
	with open("resources/files/changelog.txt", "r") as f:
		lines = f.readlines()
		if version == "latest":
			version = lines[0][:-1]
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
