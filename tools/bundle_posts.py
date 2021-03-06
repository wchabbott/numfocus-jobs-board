import yaml
import json
import glob
import sys
import datetime
import os


class JSONEncoder(json.JSONEncoder):
    #Override the default method
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()

jobs = []
for job in glob.glob("jobs/*.yaml"):
    print(f"-> {job}")
    # We could also allow specification of date inside job post file
    # For now, it is parsed from the filename
    try:
        date_str = job.split('jobs/')[1].split('_')[0]
        date = datetime.date(*(int(x) for x in date_str.split('-')))
    except Exception as e:
        print(f'Exception: {e}')
        print(f'Unable to parse date from filename {job}. Exiting.')
        sys.exit(1)

    post = yaml.load(open(job, "r"), Loader=yaml.Loader)
    post['date'] = date
    post['id'] = os.path.splitext(job)[0]
    jobs.append(post)

outfile = 'src/jobs.js'
with open(outfile, 'w') as f:
    f.write('const jobs = ')
    f.write(JSONEncoder().encode(jobs))
    f.write('\nexport default jobs;\n')

print(f'Wrote posts to [{outfile}]')
