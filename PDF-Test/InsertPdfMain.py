import os
import csv
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog

try:
    import pandas as pd
except Exception:
    pd = None

try:
    import fitz  # PyMuPDF
except Exception:
    fitz = None

try:
    from Formater import FormaterApp
except Exception:
    FormaterApp = None

selected_csv_path = ""
selected_pdf_path = ""
shared_result = ""

def load_csv(path, encoding=None):
    if pd is None:
        raise ImportError("pandas가 설치되어 있지 않습니다. 설치: pip install pandas")
    enc = encoding
    if enc is None:
        for e in ('utf-8', 'cp949', 'euc-kr'):
            try:
                df = pd.read_csv(path, encoding=e)
                return df
            except Exception:
                pass
        raise ValueError("CSV 파일을 읽을 수 없습니다. 인코딩을 확인하세요.")
    return pd.read_csv(path, encoding=enc)

def populate_tree(tree, df, max_rows=1000):
    # 컬럼 설정 초기화
    cols = list(df.columns)
    tree.delete(*tree.get_children())
    tree['columns'] = cols
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor='w')

    # 데이터 삽입
    for _, row in df.head(max_rows).iterrows():
        iid = str(_)
        tree.insert('', 'end', iid=iid, values=[str(v) for v in row.values])

def create_app():

    root = tk.Tk()
    root.title('PDF Dcoument Text Inserter')
    root.geometry('900x700+10+10')

    top_frame = ttk.Frame(root, padding=6)
    top_frame.pack(fill='x')

    btn_open = ttk.Button(top_frame, text='파일 열기 (CSV)')
    btn_save = ttk.Button(top_frame, text='CSV 저장')
    btn_clear = ttk.Button(top_frame, text='PDF 파일 선택')
    btn_select = ttk.Button(top_frame, text='PDF 파일 생성 및 열기')
    btn_makeformat = ttk.Button(top_frame, text='양식 설정 하기')

    btn_quit = ttk.Button(top_frame, text='종료', command=root.destroy)

    btn_open.pack(side='left', padx=4)
    #btn_save.pack(side='left', padx=4)
    btn_clear.pack(side='left', padx=4)
    btn_select.pack(side='left', padx=4)
    btn_makeformat.pack(side='left', padx=4)
    btn_quit.pack(side='right', padx=4)

    left_frame = ttk.Frame(root)
    left_frame.pack(fill='both', expand=True, padx=6, pady=6)

    tree = ttk.Treeview(left_frame, show='headings')
    vsb = ttk.Scrollbar(left_frame, orient='vertical', command=tree.yview)
    hsb = ttk.Scrollbar(left_frame, orient='horizontal', command=tree.xview)
    tree.configure(yscroll=vsb.set, xscroll=hsb.set)
    tree.grid(row=0, column=0, sticky='nsew')
    vsb.grid(row=0, column=1, sticky='ns')
    hsb.grid(row=1, column=0, sticky='ew')
    left_frame.grid_rowconfigure(0, weight=1)
    left_frame.grid_columnconfigure(0, weight=1)

    status_var = tk.StringVar(value='Ready')
    status = ttk.Label(root, textvariable=status_var)
    status.pack(fill='x')

    # 전역(앱 상태) 변수: df, pdf_path, font_path
    pdf_var = tk.StringVar(value='')
    font_var = tk.StringVar(value='')
    last_out_var = tk.StringVar(value='')
    lbl_pdf = ttk.Label(top_frame, textvariable=pdf_var)
    lbl_pdf.pack(side='right', padx=8)
    lbl_font = ttk.Label(top_frame, textvariable=font_var)
    lbl_font.pack(side='right', padx=8)
    lbl_out = ttk.Label(top_frame, textvariable=last_out_var)
    lbl_out.pack(side='right', padx=8)

    app_state = {'df': None, 'pdf_path': None, 'last_out_pdf': None}

    def on_open():
        global selected_csv_path
        csv_path = filedialog.askopenfilename(title='CSV 파일 선택', filetypes=[('CSV files','*.csv'), ('All','*.*')])
        selected_csv_path = csv_path
        if not csv_path:
            status_var.set('파일 선택 취소')
            return
        try:
            df = load_csv(csv_path)
            app_state['df'] = df
            populate_tree(tree, df)
            status_var.set(f'Loaded: {csv_path}  Rows: {len(df)}')
        except Exception as e:
            messagebox.showerror('Error', str(e))
            status_var.set('로드 실패')

    def on_csv_save():
        # Save current CSV using the TreeView content (this ensures in-place edits are preserved)
        path = filedialog.asksaveasfilename(title='CSV로 저장', defaultextension='.csv', filetypes=[('CSV files','*.csv'), ('All','*.*')])
        if not path:
            return
        try:
            cols = list(tree['columns'])
            rows = []
            iids = []
            for item in tree.get_children():
                vals = list(tree.item(item).get('values', []))
                # normalize length
                if len(vals) < len(cols):
                    vals = vals + [''] * (len(cols) - len(vals))
                elif len(vals) > len(cols):
                    vals = vals[:len(cols)]
                rows.append(vals)
                iids.append(item)

            with open(path, 'w', newline='', encoding='utf-8-sig') as f:
                writer = csv.writer(f)
                writer.writerow(cols)
                for r in rows:
                    writer.writerow(r)

            # If pandas is available, update the in-memory DataFrame to reflect Tree contents
            if app_state.get('df') is not None and pd is not None:
                try:
                    new_df = pd.DataFrame(rows, columns=cols)
                    # preserve original index iids when possible
                    if len(iids) == len(new_df):
                        new_df.index = iids
                    app_state['df'] = new_df
                except Exception:
                    pass

            status_var.set(f'Saved CSV: {os.path.basename(path)}')
            messagebox.showinfo('저장완료', f'CSV 파일을 저장했습니다:\n{path}')
        except Exception as e:
            messagebox.showerror('Error', str(e))
            status_var.set('CSV 저장 실패')

    def on_pdf_selection():
        global selected_pdf_path
        pdf_path = filedialog.askopenfilename(title='PDF 파일 선택', filetypes=[('PDF files','*.pdf'), ('All','*.*')])
        selected_pdf_path = pdf_path
        if not pdf_path:
            messagebox.showwarning('경고', 'PDF 파일이 선택되지 않았습니다.')
            return
        # 전역 상태에 저장
        app_state['pdf_path'] = pdf_path
        pdf_var.set(os.path.basename(pdf_path))
        status_var.set(f'PDF selected: {pdf_var.get()}')

    def on_pdf_insert_text(doc, cols, values, match):
        idx = cols.index(match)
        pages = values[idx].split(';')
        for pp in pages:
            p_text = pp.split(':')
            page = doc[int(p_text[0])-1]
            page.insert_font("gulim", "C:\\Windows\\Fonts\\gulim.ttc")
            icols =  p_text[1].split('=')
            xy = icols[1].split('.')
            x = int(xy[0])
            y = int(xy[1])
            size = int(xy[2])
            page.insert_text((x, y), str(values[cols.index(icols[0])]), fontsize=size, fontname="gulim", color=(0.0, 0.0, 0.0))

    def on_select():
        pdf_path = app_state.get('pdf_path')
        if not pdf_path:
            messagebox.showwarning('경고', '먼저 PDF 파일을 선택하거나 행에서 PDF 경로를 가져오세요.')
            return
        if not os.path.exists(pdf_path):
            messagebox.showerror('Error', f'PDF 파일을 찾을 수 없습니다: {pdf_path}')
            return
        sels = tree.selection()
        if not sels:
            messagebox.showwarning('경고', '선택된 행이 없습니다.')
            return
        item = tree.item(sels[0])
        values = item.get('values', [])
        cols = tree['columns']

        try:
            doc = fitz.open(pdf_path)
            
            # 아래 for문에서 Page = doc[n] 변경 후에 Page별 위치 설정으로 Text 삽입
            # 선택 행의 내용을 PDF 첫 페이지에 간단히 적음
            match = os.path.basename(pdf_path)
            
            if match in cols:
                
                on_pdf_insert_text(doc, cols, values, match)
                out_pdf = pdf_path.replace('.pdf', f'_{str(values[0])}.pdf')
                doc.save(out_pdf)
                doc.close()
                # 마지막으로 생성한 out_pdf 경로 저장 및 표시
                app_state['last_out_pdf'] = out_pdf
                last_out_var.set(os.path.basename(out_pdf))
                # 생성된 PDF를 기본 뷰어로 자동 열기 (Windows)
                try:
                    os.startfile(out_pdf)
                except Exception:
                    pass
                messagebox.showinfo('완료', f'PDF에 선택 내용이 기록된 파일을 저장했습니다:\n{out_pdf}')
                status_var.set(f'Wrote & opened: {os.path.basename(out_pdf)}')
            else:
                messagebox.showwarning('경고', '선택한 PDF 파일은 양식이 없습니다.')
                status_var.set('선택한 PDF 파일은 양식이 없습니다.')               
        except Exception as e:
            messagebox.showerror('Error', str(e))
            status_var.set('PDF 쓰기 실패')

    def on_makeformat():
        if "" == selected_csv_path or "" == selected_pdf_path:
            messagebox.showwarning('경고', 'CSV 파일과 PDF 파일을 먼저 선택하세요.')
            return
        global shared_result
        shared_result = ""
        format_app = FormaterApp(root, selected_csv_path, selected_pdf_path, shared_result)


    btn_open.config(command=on_open)
    #btn_save.config(command=on_csv_save)
    btn_clear.config(command=on_pdf_selection)
    btn_select.config(command=on_select)
    btn_makeformat.config(command=on_makeformat)

    return root

if __name__ == '__main__':

    app = create_app()
    app.mainloop()