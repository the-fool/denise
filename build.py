import make_yaml
import csv


with open('portfolios.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        path = row[0]
        title = row[1]
        yaml = make_yaml.make_yaml(path=path, title=title)

        with open(f'content/portfolios/{path}.md', 'w') as outfile:
            outfile.write(yaml)
        
