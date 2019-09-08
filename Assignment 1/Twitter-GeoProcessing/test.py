import pandas as pd

def split_file(path, n):
    df = pd.read_table(path, iterator=True)
    print(df)
    loop = True
    chunks = []
    while loop:
        try:
            chunk = df.get_chunk(n)
            print(chunk)
            chunks.append(chunk)
        except:
            loop = False
    return chunks

split_file('../tinyTwitter.json', 100)