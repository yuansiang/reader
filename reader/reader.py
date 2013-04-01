import json
import re
from xml.dom import minidom
import webapp2

class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.out.write('''
	  
	<!DOCTYPE html>
    <head>
        <meta charset="utf-8">
		<link href='http://fonts.googleapis.com/css?family=Lato:400,900' rel='stylesheet' type='text/css'>
        <title>Reader</title>
        <link rel="stylesheet" href="/static/style.css">
    </head>
    <body>
		<header><h1>reaDHS</h1></header>
		<article>
		''')
		#import files
		infile = open("what%27s-new--19.xml","r")
		xml = infile.read()

		#get channels
		xml_data = minidom.parseString(xml).getElementsByTagName('channel')
		#get news
		parts = xml_data[0].getElementsByTagName('item')
		all ={}
		jsonparts = [all]

		for part in parts:
			# get title
			title = part.getElementsByTagName('title')[0].firstChild.nodeValue.strip()
			# get link
			link = part.getElementsByTagName('link')[0].firstChild.nodeValue.strip()
			# get description
			description = part.getElementsByTagName('description')[0].firstChild.wholeText.strip()
			description = re.sub("<[^>]*>", "", description)
			description = description[:-12]
			# display info
			#jsonparts.append({"title":title, "link":link, "description":description})
			all[title] = [link, description]
			#print "\n".join([title, link, description, ""])

		#encode
		encoded = json.dumps(jsonparts, sort_keys=True, indent=2)
		#print encoded
		decoded = json.loads(encoded)
		infile.close()
		for part in decoded[0]:
			self.response.out.write('''
				<section>
				<a target="_blank" href = "''')
			#link
			self.response.out.write(decoded[0][part][0])
			self.response.out.write(''' ">''')
			#title
			self.response.out.write(part)
			self.response.out.write('''</a><p>''')
			#description
			self.response.out.write(decoded[0][part][1])
			self.response.out.write('''</p>''')
			self.response.out.write('''</section>''')

		self.response.out.write('''
		</article>
		</body>
		</html>''')


app = webapp2.WSGIApplication([('/', MainPage)
							   ]
							   ,
                               debug=True)