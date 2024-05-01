from textnode import TextNode
import os
import shutil
from pathlib import Path
from block import markdown_to_html_node

root_dir = Path(__file__).resolve().parent.parent


def main():
    test_node = TextNode("This is a text node", "bold", "https://www.boot.dev")

    print(test_node)

    print(root_dir)
    # Remove /public if exist
    if os.path.exists(f"{root_dir}/public"):
        shutil.rmtree(f"{root_dir}/public")
    # Create directory
    os.mkdir(f"{root_dir}/public")

    copy_static()

    extract_title(os.path.join(root_dir, "content", "index.md"))

    generate_page_recursive("content", "template.html", "public")
    print("end")


def copy_static(path="."):
    src_path = os.path.join(root_dir, "static", path)
    list_entries = os.listdir(src_path)
    for entry in list_entries:
        if os.path.isfile(os.path.join(src_path, entry)):
            shutil.copy(
                os.path.join(src_path, entry), os.path.join(root_dir, "public", path)
            )
        else:
            os.mkdir(os.path.join(root_dir, "public", entry))
            copy_static(os.path.join(path, entry))


def extract_title(markdown):
    with open(markdown, "r") as f:
        for line in list(f):
            if line.startswith("#"):
                line.rstrip("\n")
                return line
    raise Exception("No h1 header found in the input markdown file")


def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    from_content = None
    with open(os.path.join(root_dir, from_path), "r") as fc:
        from_content = fc.read()

    template_content = None
    with open(os.path.join(root_dir, template_path), "r") as tc:
        template_content = tc.read()

    print("Read and saved both contents")

    html_node_from_content = markdown_to_html_node(from_content)
    print("Converted markdown to HTMLnode")

    html_from_content = html_node_from_content.to_html()
    print("Converted HTMLnode to string")

    title = extract_title(from_path)
    print("Extracted title")

    replaced_content = template_content.replace("{{ Title }}", title).replace(
        "{{ Content }}", html_from_content
    )

    dir_path = dest_path.rsplit("/", 1)[0]

    os.makedirs(os.path.join(root_dir, dir_path), exist_ok=True)

    wf = open(os.path.join(root_dir, dest_path), "w")
    wf.write(replaced_content)
    wf.close()


def generate_page_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str
):
    print(
        f"Generating pages recursibely from {dir_path_content} to {dest_dir_path} using {template_path}"
    )

    src_path = os.path.join(root_dir, dir_path_content)
    list_entries = os.listdir(src_path)
    for entry in list_entries:
        if os.path.isfile(os.path.join(src_path, entry)):
            generate_page(
                os.path.join(src_path, entry),
                template_path,
                os.path.join(root_dir, dest_dir_path, f"{entry.rsplit('.',1)[0]}.html"),
            )
        else:
            os.mkdir(os.path.join(root_dir, "public", entry))
            generate_page_recursive(
                os.path.join(dir_path_content, entry),
                template_path,
                os.path.join(dest_dir_path, entry),
            )


main()
