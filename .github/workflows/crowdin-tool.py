import os
import json
import re
from crowdin_api import CrowdinClient

# setup variables
project_token = os.environ['crowdin_api_token']
PROJECT_ID = 570269
STABLEDIFFUSION_DIR_ID = 457
EXTENSION_DIR_ID = 459

# fetch all crowdin source files
client = CrowdinClient(token=project_token)
stablediffusion_files = client.source_files.with_fetch_all(
).list_files(projectId=PROJECT_ID, directoryId=STABLEDIFFUSION_DIR_ID)
extension_files = client.source_files.with_fetch_all(
).list_files(projectId=PROJECT_ID, directoryId=EXTENSION_DIR_ID)


def crowndin(file_scope):
    progress_list = []
    # get file progress and print to markdown strings
    for idx, filedata in enumerate(file_scope['data']):
        # setting variables
        file_id = filedata['data']['id']
        file_name = filedata['data']['name'].replace('.json', '')
        file_path = filedata['data']['path'].replace('/translations/', './')
        file_progress = client.translation_status.get_file_progress(
            projectId=PROJECT_ID, fileId=file_id)['data'][0]['data']['translationProgress']
        check_box = '[ ]'
        if file_progress == 100:
            check_box = '[x]'

        # Get extension url
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)

                # find key contains 'http' and convert to url
                url_pattern = re.compile(r"https://github.com/([^/\s]+)/([^/\s]+)")
                extension_url = ''
                for key in data.keys():
                    if file_name == 'StableDiffusion':
                        extension_url = 'https://github.com/AUTOMATIC1111/stable-diffusion-webui'
                    elif file_name == 'ExtensionList':
                        extension_url = 'https://raw.githubusercontent.com/wiki/AUTOMATIC1111/stable-diffusion-webui/Extensions-index.md'

                    if 'https' in key:
                        matches = re.findall(url_pattern, key)
                        for match in matches:
                            username, repository = match
                            if '.git' in repository:
                                repository = repository.replace('.git', '')
                            file_repo = file_name.replace('.json', '')
                            if file_repo == repository:
                                extension_url = f"https://github.com/{username}/{repository}"
        else:
            print(f"url not found at '{file_path}'")

        progress_list.append(
            f"- {check_box} ![{file_name} translated {file_progress}%](https://geps.dev/progress/{file_progress}?dangerColor=c9f2dc&warningColor=6cc570&successColor=00ff7f) [{file_name}]({extension_url})")
        print(
            f"[{idx+1}/{len(file_scope['data'])}] {file_name} translation progress fetch success.")
    return progress_list


# read README.md
with open('./README.md', 'r', encoding='utf-8') as file:
    readme_content = file.read()

# extract contents without progress section
start_index = readme_content.find('# 本地化進度')
end_index = readme_content.find('# 安裝說明')
top_content = readme_content[0:start_index]
bottom_content = readme_content[end_index:len(readme_content)]

# generating new progress content
MIDDLE_CONTENT = '# 本地化進度\n\n<details>\n<summary>Stable Diffusion web UI 本地化進度</summary>\n\n'
for string in crowndin(stablediffusion_files):
    MIDDLE_CONTENT += f"{string}\n"
MIDDLE_CONTENT += '</details>\n\n<details>\n<summary>擴充功能本地化進度</summary>\n\n'
for string in crowndin(extension_files):
    MIDDLE_CONTENT += f"{string}\n"
MIDDLE_CONTENT += '</details>\n\n'

# write new contents back to README.md
new_content = top_content+MIDDLE_CONTENT+bottom_content
with open('./README.md', 'w', encoding='utf-8') as readme:
    readme.write(new_content)