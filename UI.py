import tkinter as tk
from main import calc_similarity, get_docs_matrix


# Define the search function
def search_query(query, dataset, result_list):
    result_list.delete(0, tk.END)  # Clear the previous search results
    results,result_to_show = calc_similarity(query, get_docs_matrix("tfidf[docs]"+dataset+".pickle"), '[vectorizer]'+dataset+'.pickle',get_docs_matrix("tfidf[doc_key]"+dataset+".pickle") ,get_docs_matrix("tfidf[doc_value]"+dataset+".pickle"))
    # results=['aya','leen']
    for result in result_to_show:
        result_list.insert(tk.END, result)

# Define the function to handle dataset selection
def select_dataset(dataset):
    print(f"Selected dataset: {dataset}")
    if dataset == "antique":
        # Add your code here to perform a specific action for the Antique dataset
        print("Performing action for Antique dataset...")

    else:
        # Add your code here to perform a specific action for the WikIR1k dataset
        print("Performing action for WikIR1k dataset...")



    root.destroy()  # Close the dataset selection interface
    # Create the search interface
    search_root = tk.Tk()
    search_root.title("Search Engine Interface")

    # Create the search box
    entry = tk.Entry(search_root,width=200)
    entry.pack()

    # Create the search button
    button = tk.Button(search_root, text="Search", command=lambda: search_query(entry.get(), dataset, result_list))
    button.pack()

    # Create the list of results
    result_list = tk.Listbox(search_root, width=200,height=200)
    result_list.pack()

    # Start the main event loop for the search interface
    search_root.mainloop()

# Create the main window
root = tk.Tk()
root.title("Dataset Selection")

# Create the dataset selection buttons
button1 = tk.Button(root, text="antique", command=lambda: select_dataset("antique"))
button1.pack(side=tk.LEFT)
button2 = tk.Button(root, text="wikIR1k", command=lambda: select_dataset("wikIR1k"))
button2.pack(side=tk.LEFT)

# Start the main event loop for the dataset selection interface
root.mainloop()