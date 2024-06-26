# TreeNote - A Tree Structure Note-taking Application

![](https://github.com/NejsemTonda/treeNote/blob/main/src/showcase1.png)

## Motivation

I wanted to create an app where I would be comfortable making notes. I didn't like the fact that I don't have any perspective in my notes, and when I write them in one file, I often get lost in them. I really liked the tree-like structure of the notes, like in Obsidian.md. I wanted to use Vim as a text editor because it suits me the most of all text editors. But I didn't find any application that suited me perfectly, so I decided to create my own.

### How to Run

1. install requirements: `pip install -r requirements.txt`
    * Don't forget about pandoc and pdftoppm on you linux machine
2. run init: `python3 treeNote.py --init`
3. everytime after first run: `python3 treeNote.py`

### Controls

- Click on the node you wish to edit. The currently loaded node should be highlighted with a different color.
- Hover the mouse over the node you wish to see its thumbnail.
- Click and drag on the background to shift all nodes.
- Click and drag on a node to move the node and its children.
- Ctrl+click on the background to create a new node.
- Ctrl+click on a node to create new children of this node.


see more in documentation (Not ready yet) (https://github.com/NejsemTonda/treeNote/blob/main/documentation/documentation.md)

### TODO's

* Improve Node object design (add inharitance)
* Nodes collides with deleted nodes? Or with thumbnail of deleted nodes
* Save `.session` on error
* Throws an error when 2 nodes have same name 
