import pathlib

p = pathlib.Path(r'C:\Users\Ailyn Nicol\Desktop\Ailyn-Gomez-Dev\assets\top-langs.svg')
content = p.read_text(encoding='utf-8')

content = content.replace('height="165"', 'height="195"')
content = content.replace('viewBox="0 0 350 165"', 'viewBox="0 0 350 195"')
content = content.replace('transform="translate(25, 35)"', 'transform="translate(25, 42)"')
content = content.replace('transform="translate(0, 55)"', 'transform="translate(0, 68)"')

p.write_text(content, encoding='utf-8')
print("Successfully updated top-langs.svg to height 195px")
