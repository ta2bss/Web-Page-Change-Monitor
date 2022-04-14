from bs4 import BeautifulSoup

def is_visible_span_or_div(tag, is_parent=False):
    """ This function checks if the element is a span or a div,
    and if it is visible. If so, it recursively checks all the parents
    and returns False is one of them is hidden """

    # loads the style attribute of the element
    style = tag.attrs.get('style', False)

    # checks if element is div or span, if it's not a parent
    if not is_parent and tag.name not in ('div', 'span'):
        return False

    # checks if the element is hidden
    if style and ('hidden' in style or 'display: none' in style):
        return False

    # makes a recursive call to check the parent as well
    parent = tag.parent
    if parent and not is_visible_span_or_div(parent, is_parent=True):
        return False

    # neither the element nor its parent(s) are hidden, so return True
    return True

html = """
    <span style="display: none;">I am not visible</span>
    <span style="display: inline">I am visible</span>
    <div style="display: none;">
        <span>I am a visible span inside a hidden div</span>
    </div>
"""

soup = BeautifulSoup(html)

visible_elements = soup.find_all(is_visible_span_or_div)

print(visible_elements)