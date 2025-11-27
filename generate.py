import os
import glob
import base64
from random import shuffle
from jinja2 import Environment, FileSystemLoader

env = Environment(
    loader=FileSystemLoader("templates")
)
env.globals.update(zip=zip)

# Make sure docs/ exists
os.makedirs("docs", exist_ok=True)

for html_file in glob.glob(os.path.join("docs", "*.html")):
    os.remove(html_file)

days = list(range(1, 25))
shuffle(days)
day_filenames = [
    f"day{day}_{base64.urlsafe_b64encode(os.urandom(32)).decode('utf-8')}"
    for day in days
]

# Load HTML template

day_template = env.get_template("day_template.html")

# Generate 24 pages
for day, day_filename in zip(days, day_filenames):
    day_content = day_template.render(day=day)
    with open(os.path.join("docs", f"{day_filename}.html"), "w", encoding="utf-8") as file:
        file.write(day_content)


index_template = env.get_template("index_template.html")

index_content = index_template.render(days=days, day_filenames=day_filenames)
with open(os.path.join("docs", "index.html"), "w", encoding="utf-8") as file:
    file.write(index_content)

print("Calendar generated successfully!")
