import AO3
import datetime as dt
import webbrowser

def has_update(work,last_checked):
    ## Returns True if work has updated on or since last_checked
    ## AO3.Work Datetime -> Bool
    last_updated = work.date_updated # request from AO3 (1/ work)
    return last_updated>=last_checked # Bigger than means after

def is_incomplete(work):
    ## Returns True if work is incomplete
    ## AO3.Work -> Bool
    return work.status == "Work in Progress"

def get_objects_from_file(file_name,constructor):
    ## Returns a list of objects made with constructor from file_name,
    ##  or empty list if file_name does not exist
    ## Requires: constructor takes only one input
    ## Str Func -> (listof Any)
    try:
        with open(file_name) as a:
            return list(map(constructor, a.readlines()))
    except OSError:
        # print("There is no file called",file_name+"; returning blank list.") # Debug only
        return []

def remove_completed_works(work_file_name,tracked_works):
    ## Re-writes work_file_name to be without any complete works in tracked_works
    ## Str (listof AO3.Work) -> None
    still_incomplete = list(filter(is_incomplete,tracked_works))
    with open(work_file_name,"w") as f:
        f.writelines(list(map(lambda w: w.id, still_incomplete)))

def get_all_works_from_multiple_authors(listof_authors):
    ## Returns a list of all works by all authors in listof_authors
    ## (listof AO3.User) -> (listof AO3.Work)
    works_by_authors = []
    for author in listof_authors:
        works_by_authors.extend(author.get_works())
    return works_by_authors

def get_all_updated_works(author_objects,work_objects,date_last_checked):
    ## Returns a list of all works by all authors in author_objects and 
    ##   all works in work_objects that have been published or updated 
    ##   on or after date_last_checked
    ## (listof AO3.User) (listof AO3.Work) Datetime -> (listof AO3.Work)
    work_objects_by_authors = get_all_works_from_multiple_authors(author_objects)

    all_work_objects = []
    all_work_objects.extend(work_objects)
    all_work_objects.extend(work_objects_by_authors)

    updated_work_objects = list(filter(lambda work: has_update(work,date_last_checked), all_work_objects))

    return updated_work_objects

def repr_work_from_template(work,template):
    ## Returns a representation of work according to template
    ## Requires: template contains fields for url, title, and authors of work, and no more
    ## AO3.Work Str -> Str
    url = work.url
    title = work.title
    authors = list(map(lambda a: a.username, work.authors))
    authors_str = ", ".join(authors)
    return template.format(url=url,title=title,authors=authors_str)

def make_html(works,element_template,web_template,output_file_name,since_date):
    ## Creates an HTML file named output_file_name listing each item in works as 
    ##   an element like in the file named element_template. The file is made
    ##   according to web_template and contains since_date
    ## (listof AO3.Work) Str Str Datetime -> None
    with open(web_template) as t:
        web_template = "\n".join(t.readlines())

    with open(element_template) as t:
        element = "\n".join(t.readlines())

    elements = list(map(lambda w: repr_work_from_template(w,element),works))

    body_date = "<time datetime="+str(since_date)+">"+str(since_date)+"</time>"
    body_elements = "".join(elements)

    web_page = web_template.format(elements=body_elements,datetime=body_date)

    with open(output_file_name,"w") as f:
        f.write(web_page)

if __name__ == "__main__":
    date_format = "%Y-%m-%d"
    last_checked_file_name = "data/last_ran.txt"
    with open(last_checked_file_name) as f:
        date_text = f.readline()[:10]
        date = dt.datetime.strptime(date_text,date_format)
    
    file_name_authors_global = "data/authors.txt"
    file_name_works_global = "data/works.txt"
    
    author_objects_global = get_objects_from_file(file_name_authors_global,AO3.User)
    work_objects_global = get_objects_from_file(file_name_works_global,AO3.Work)

    remove_completed_works(file_name_works_global,work_objects_global)

    works_list = get_all_updated_works(author_objects_global,work_objects_global,date)

    file_name_element = "resource/element.html"
    file_name_web = "resource/web_template.html"
    file_name_output = "updates.html"
    make_html(works_list,file_name_element,file_name_web,file_name_output,date)

    with open(last_checked_file_name,"w") as f:
        f.write(str(dt.datetime.now())[:10])
    
    webbrowser.open_new_tab(file_name_output)
