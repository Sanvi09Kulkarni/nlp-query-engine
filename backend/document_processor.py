class DocumentProcessor:
    def __init__(self):
        self.docs = []

    def process_files(self, files):
        for f in files:
            raw = f.file.read()
            try:
                text = raw.decode("utf-8")
            except:
                text = str(raw)
            self.docs.append({"id": len(self.docs)+1, "text": text})

