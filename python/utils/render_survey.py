template_filename = 'test_html_survey.jinja2'  # Replace with your template filename

# from jinja2 import Environment, Template
# from jinja2.filters import environmentfilter
import json

import yaml

# # Define a custom filter to mark content as safe
# @environmentfilter
# def safe_filter(environment, value):
#     return environment.markupsafe.Markup(value)

# Define the survey JSON (replace with your actual survey definition)
# survey_definition = {
#     "pages": [
#         {
#             "name": "page1",
#             "title": "Page 1",
#             "elements": [
#                 {
#                     "type": "text",
#                     "name": "name",
#                     "title": "Your Name"
#                 }
#             ]
#         },
#         {
#             "name": "page2",
#             "title": "Page 2",
#             "elements": [
#                 {
#                     "type": "radiogroup",
#                     "name": "experience",
#                     "title": "Your Experience",
#                     "choices": ["Beginner", "Intermediate", "Advanced"]
#                 }
#             ]
#         }
#     ]
# }

# Specify the path to your YAML file
yaml_file_path = 'survey.yaml'

# Open and read the YAML file
with open(yaml_file_path, 'r') as yaml_file:
    survey_definition = yaml.load(yaml_file, Loader=yaml.FullLoader)

# Now, yaml_data contains the parsed YAML content as a Python dictionary
# print(json.dumps(yaml_data, indent=4))

# Convert the survey JSON to a pretty printed string
survey_json_str = json.dumps(survey_definition, indent=4)

# Define the path to your Jinja2 template file
# template_filename = 'test_html_survey.jinja2'  # Replace with your template filename

# Load the Jinja2 template from the file
with open(template_filename, 'r') as template_file:
    template_content = template_file.read()

# use {{{survey_json}}} because jinja is not working well with pretty printed json
template_content = template_content.replace("{{{survey_json}}}", survey_json_str)

# Create a Jinja2 template object
# jinja_template = Template(template_content)

# # Render the Jinja2 template with the pretty printed JSON (using the safe filter)
# rendered_template = jinja_template.render(survey_json=survey_json_str)

# # Render the Jinja2 template with the survey JSON
# template = env.get_template('survey_template.html')
# rendered_template = jinja_template.render(survey_json=survey_definition)

# Print or use the rendered template as needed (e.g., serve it via a web framework)

# Specify the file name
file_name = "SurveyComponent.jsx"

# Open the file for writing
with open(file_name, "w") as file:
    # Write the content to the file
    file.write(template_content)
print(f"Rendered template written to {file_name}")



