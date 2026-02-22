from tkinter import filedialog, Tk, Label, Button, StringVar, messagebox
import os
import shutil

root = Tk()
root.withdraw()

def select_origin():
    origin = filedialog.askdirectory(initialdir = '', title='Selecione a pasta para organizar')
    return origin

def scan_folder(path):
    list_dir = os.listdir(path)
    dict_extension_files = dict()
    num_files = 0
    num_folders = 0

    for files in list_dir:
        full_path = os.path.join(path, files)
        
        if os.path.isfile(full_path):
            name, extension = os.path.splitext(files)
            extension = extension.lower()

            if extension not in dict_extension_files:
                dict_extension_files[extension] = []
            dict_extension_files[extension].append(files)
            num_files += 1
        else:
            num_folders += 1
    if '' in dict_extension_files:
        dict_extension_files['Sem extensão'] = dict_extension_files.pop('')

    dict_extension_files = sorted(dict_extension_files.items())
    return dict(dict_extension_files), num_files, num_folders

def map_interface(dict_extension_file):

    def choose_func(e, s):
        path = filedialog.askdirectory()
        chooses[e] = path
        s.set(f'Caminho selecionado: {path}')

    root = Tk()
    root.geometry('600x400')
    chooses = {}

    for row, extension in enumerate(dict_extension_file):
        selection = StringVar()

        label = Label(root, text=extension)
        button = Button(root, text="Selecionar destino", command=lambda e=extension, s=selection: choose_func(e, s))
        selection_label = Label(root, textvariable=selection) 
 

        label.grid(row=row, column=0)
        button.grid(row=row, column=1)
        selection_label.grid(row=row, column=2)

    quit = Button(root, text='Iniciar organização.', command=root.destroy)
    quit.grid(row=100)

    root.mainloop()

    return chooses

def merge(chooses, dict_extension_file, origin):

    files_error = []

    for extensions, path in chooses.items():
        if path:
            os.makedirs(path, exist_ok=True)
            for files in dict_extension_file[extensions]:

                new_name = files
                count = 1

                while os.path.exists(os.path.join(path, new_name)):
                    name, ext = os.path.splitext(files)
                    new_name = f'{name}_{count}{ext}'
                    count += 1
                
                try:
                    shutil.move(os.path.join(origin, files), os.path.join(path, new_name))
                except:
                    files_error.append(files)
                    pass
    
    return files_error

def ask_to_continue():
    return messagebox.askyesno("Continuar?", 'Deseja organizar outra pasta?')

def main():
    while True:
        while True:
            origin = select_origin()
            if origin:
                break
            messagebox.showwarning('Erro!', 'Você deve selecionar uma pasta!')
        
        dict_extension_file, num_files, num_folders = scan_folder(origin)

        if num_files > 0:
            chooses = map_interface(dict_extension_file)
            if chooses > 0:
                files_error = merge(chooses, dict_extension_file, origin)
                if len(files_error) > 0:
                    messagebox.showwarning('Aviso!', f'Os arquivos {files_error} não puderam ser movidos! Tente manualmente!')

                num_end_folders = set(chooses.values())
                messagebox.showinfo('Sucesso!', f'Sucesso! {num_files} foram movidos para {len(num_end_folders)} pastas. \n {num_folders} pastas na pasta principal não foram organizadas!')

            else:
                print('OMG')
                pass
        print('here')
        if not ask_to_continue():
            break

main()
