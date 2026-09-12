def add_student(name, *arg):
    skills = list(arg)
    skills.append("Python")
    return {
        "name": name,
        "skills": skills
    }


a = add_student("Tom", "vue")
b = add_student("Lucy", "java")

print(a)
print(b)
