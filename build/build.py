from glob import glob
from markdown import markdown
import math 
import os 


def build_general(source_md, replace_hr=True):
    '''If replace_hr=True, writing ---- in Markdown will create a separate
    entry box.
    '''
    content_html_fmt = '''
        <div class="entry">
            {}
        </div>'''
    file = open(source_md, 'r')
    content = file.read().strip()
    content_html = markdown(content)

    if replace_hr:
        replace = '</div>\n<div class="entry">'
        content_html = content_html.replace('<hr />', replace)

    content_html = content_html_fmt.format(content_html)

    return content_html


def build_index():
    posts_path = 'posts/{}.md'
    posts = glob(posts_path.format('*'))

    # Title formatting
    digits_in_index = int(math.floor(math.log10(len(posts))))
    title_string = '{{:0{}d}}_{{}}'.format(digits_in_index + 1)

    index_title_html_fmt = '<li><a href="#{0}">{0}</a></li>'
    index_html_fmt = '''
        <div class="entry">
            <h2>index</h2>
            <p>
            <ul>
                {}
            </ul>
            </p>
        </div>'''

    entry_title_html_fmt = '<h2 id="{0}">{0}</h2>'
    entry_html_fmt = '''
        <div class="entry">
            {}
        </div>'''

    index_html = []
    entries_html = []
    for i in range(len(posts)):
        file = open(posts_path.format(i), 'r')

        # Create title strings
        title = file.readline().strip().lower()
        title = '_'.join(title.split(' '))
        title = title_string.format(i, title)
        index_title_html = index_title_html_fmt.format(title)
        entry_title_html = entry_title_html_fmt.format(title)
        
        # Convert post content to HTML
        entry_content = file.read().strip()
        entry_content_html = markdown(entry_content)

        # Create entry
        entry_html = '{}\n\n{}'.format(entry_title_html, entry_content_html)
        entry_html = entry_html_fmt.format(entry_html)

        index_html.append(index_title_html)
        entries_html.append(entry_html)

    index_html = '\n'.join(index_html[::-1])
    index_html = index_html_fmt.format(index_html)
    entries_html = '\n'.join(entries_html[::-1])
    content_html = '\n'.join([index_html, entries_html])

    return content_html


def write_html(content, pagename, css):
    template = open('template.html', 'r').read()
    output = template.replace('BACKGROUND', pagename)
    output = output.replace('<!-- CONTENT -->', content)

    css_tmp = '<link href="{}" rel="stylesheet">'
    css_files = [css_tmp.format(css_file) for css_file in css]
    css_files = '\n'.join(css_files)
    output = output.replace('<!-- CSS -->', css_files)

    filename = pagename + '.html'
    open(filename, 'w').write(output)
    os.rename(filename, '../' + filename)


# Index
content = build_index()
write_html(content, 'index', ['css/style.css'])
