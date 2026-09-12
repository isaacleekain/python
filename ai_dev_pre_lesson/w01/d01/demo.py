project = {
    "name": "AI Search PoC",
    "members": [
        {
            "name": "Tom",
            "skills": ["Python", "SQL", "Python"],
            "active": True,
        },
        {
            "name": "Lucy",
            "skills": ["Python", "RAG", "LangGraph"],
            "active": True,
        },
        {
            "name": "Jack",
            "skills": ["AWS", "Docker", "SQL"],
            "active": False,
        },
    ],
    "tags": ["AI", "RAG", "PoC", "AI"],
}

t1 = project["name"]

t2 = project["members"][1]["skills"]

project["members"][0]["name"] = "Thomas"

project["members"][2]["skills"].append("Python")

project["tags"] = list(set(project["tags"]))

backup = project.deepcopy(project)
backup["members"][0]["name"] = "BackupUser"

Tom
BackupUser


