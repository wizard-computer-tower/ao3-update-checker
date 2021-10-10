import AO3
import datetime as dt
import webbrowser

debug = False

def has_update(work,last_checked):
    ## Returns True if work has updated since last_checked
    ## AO3.Work -> Bool
    last_edited = work.date_updated # request from AO3 (1/ work)
    return last_edited>=last_checked # Bigger than means after

def is_incomplete(work):
    ## Returns True if work is incomplete
    ## AO3.Work -> Bool
    return work.status == "Work in Progress"

def remove_completed_works(work_file_name,tracked_works):
    ## Re-writes work_file_name to be without any complete works in tracked_works
    ## Str (listof AO3.Work) -> None
    still_incomplete = list(filter(is_incomplete,tracked_works))
    with open(work_file_name,"w") as f:
        f.writelines(list(map(lambda w: w.id, still_incomplete)))

def get_all_works_from_multiple_authors(listof_authors):
    ## Returns a list of all works by all authors in the list of authors
    ## (listof AO3.User) -> (listof AO3.Work)
    works_by_authors = []
    for author in listof_authors:
        works_by_authors.extend(author.get_works())
    return works_by_authors

def get_objects_from_file(file_name,constructor):
    ## Returns a list of objects made with constructor from file_name
    ## Requires: constructor takes one input
    ## Str Func -> (listof AO3.User)
    with open(file_name) as a:
        return list(map(constructor, a.readlines()))


def get_all_updated_works(author_file_name,work_file_name,last_checked):
    ## Returns a list of all works by all authors in 
    ##   the files represented by author_file_name and work_file_name
    ## Str Str Datetime -> (listof AO3.Work)
    author_objects = get_objects_from_file(author_file_name,AO3.User)
    work_objects = get_objects_from_file(work_file_name,AO3.Work)

    work_objects_by_authors = get_all_works_from_multiple_authors(author_objects)

    all_work_objects = []
    all_work_objects.extend(work_objects)
    all_work_objects.extend(work_objects_by_authors)

    updated_work_objects = list(filter(lambda work: has_update(work,last_checked), all_work_objects))

    return updated_work_objects

def repr_work_as_li_element(work,template):
    ## Returns a representation of a given work as an HTML li element
    ## AO3.Work Str -> Str
    #work = work.reload()
    url = work.url
    title = work.title
    authors = list(map(lambda a: a.username, work.authors))
    authors_str = ", ".join(authors)
    return template.format(url=url,title=title,authors=authors_str)

def make_html(works,element_template,head_template,output_file_name,since_date):
    ## Creates an HTML file with a list of works
    ## (listof AO3.Work) Str Str -> None
    with open(head_template) as t:
        head = t.readline()

    with open(element_template) as t:
        element = t.readline()

    elements = list(map(lambda w: repr_work_as_li_element(w,element),works))

    body_date = "<time datetime="+str(since_date)+">"+str(since_date)+"</time>"
    body_start = "<body><h1>Updated since {time_element}</h1><ul>".format(time_element=body_date)
    body = body_start+"".join(elements)+"</ul></body></html>"

    with open(output_file_name,"w") as f:
        f.write(head+body)

if __name__ == "__main__" and not debug:
    date_format = "%Y-%m-%d"
    last_checked_file_name = "data/last_ran.txt"
    with open(last_checked_file_name) as f:
        date = dt.datetime.strptime(f.readline(),date_format)
    
    file_name_authors_global = "data/authors.txt"
    file_name_works_global = "data/works.txt"

    works_list = get_all_updated_works(file_name_authors_global,file_name_works_global,date)

    file_name_element = "resource/element.html"
    file_name_head = "resource/head.html"
    file_name_output = "updates.html"
    make_html(works_list,file_name_element,file_name_head,file_name_output,date)

    with open(last_checked_file_name,"w") as f:
        f.write(str(dt.datetime.now())[:10])
    
    webbrowser.open_new_tab(file_name_output)

if __name__ == "__main__" and debug:
    debug_all = False

    print("=== DEBUG DATE ===")
    debug_date = dt.datetime(2021,10,10)
    print(debug_date)

    if debug_all:

        authors = "data/authors.txt"
        works = "data/works.txt"

        debug_work_new_incomplete = AO3.Work(34013635) # published 2021-09-21 updated 2021-10-10 incomplete work
        debug_work_old_complete = AO3.Work(16483172) # published 2018-11-01 complete work

        print("\n\n=== DEBUGGING has_update ===")
        update_debug_true = has_update(debug_work_new_incomplete,debug_date) # published 2021-09-21 updated 2021-10-10
        print("Work updated 2021-10-10 should give True:",update_debug_true)

        update_debug_false = has_update(debug_work_old_complete,debug_date) # published 2018-11-01
        print("Work updated 2018-11-01 should give False:",update_debug_false)

        print("\n\n=== DEBUGGING is_incomplete ===")
        complete_debug_true = is_incomplete(debug_work_new_incomplete)
        print("Work in progress should give True:",complete_debug_true)

        complete_debug_false = is_incomplete(debug_work_old_complete)
        print("Complete work should give False:",complete_debug_false)

        print("\n\n=== DEBUGGING get_objects_from_file ===")
        work_debug = get_objects_from_file(works,AO3.Work)
        print("List of AO3 work objects\n",work_debug)

        author_debug = get_objects_from_file(authors,AO3.User)
        print("List of AO3 user objects\n",author_debug)

        print("\n\n=== DEBUGGING get_all_works_from_multiple_authors ===")
        works_by_authors_debug = get_all_works_from_multiple_authors(author_debug)
        print("List of AO3 work objects retreived from AO3 user objects\n",works_by_authors_debug)
        print("Type of first element should be AO3.Work: ",type(works_by_authors_debug[0]))

        print("\n\n=== DEBUGGING filtering updated works lambda ===")
        debug_list = [debug_work_new_incomplete,debug_work_old_complete]
        debug_filtered_list = list(filter(lambda work: has_update(work,debug_date), debug_list))
        print("Work 34013635 is called Tributary at the time I'm writing this\n",debug_filtered_list)

        print("\n\n=== DEBUGGING work.authors attribute ===")
        debug_work_author_attr = AO3.Work(11482971)
        print("Work 11482971 is by Dayanara at the time I'm writing this\n",str(debug_work_author_attr.authors))

        print("\n\n=== DEBUGGING repr_work_as_li_element ===")
        with open("resource/element.html") as t:
            template = t.readline()
        formatted_string = repr_work_as_li_element(debug_work_author_attr,template)
        print("Author should be Daranaya:",formatted_string)

        webbrowser.open_new_tab("updates.html")
