import csv

class ContactLoader(object):

    def __init__(self, contact_file):
        self.file = contact_file

    def load_contacts(self):
        with open(self.file, "r") as f:
            reader = csv.reader(f)
            contacts = []
            for row in reader:
                contacts  += row
            return contacts

    def export_contacts(self, new_contacts):
        with open(self.file, 'wb') as csvfile:
              writer = csv.writer(csvfile)
              for mem in new_contacts:
                  writer.writerow([mem])
