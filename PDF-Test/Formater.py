import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog

try:
    import fitz  # PyMuPDF
except Exception:
    fitz = None

try:
    from PIL import Image, ImageTk
except Exception:
    Image = None
    ImageTk = None

try:
    import pandas as pd
except Exception:
    pd = None

selected_csv_path = ""
selected_pdf_path = ""   
send_shared_result = ""

class FormaterApp(tk.Toplevel):

    def __init__(self, parent, csv_path, pdf_path, shared_result):
        super().__init__(parent)
        global selected_csv_path
        global selected_pdf_path
        global send_shared_result
        selected_csv_path = csv_path
        selected_pdf_path = pdf_path
        send_shared_result = shared_result
        self.parent = parent
        self.root = self
        self.root.title("PDF Formater")  
        self.root.geometry('970x990+930+10')
        self.container = self.root
        self.result = ""
        self.top = ttk.Frame(self.container, padding=6)
        self.top.pack(fill='x')
        self.top_option = ttk.Frame(self.container, padding=6)
        self.top_option.pack(fill='x')

        # 'PDF 열기' 버튼은 임베드 시 제거됨; 외부에서 load_pdf(path)를 호출하세요.
        self.page_var = tk.IntVar(value=1)
        self.spin_page = ttk.Spinbox(self.top, from_=1, to=1, textvariable=self.page_var, width=6)
        self.spin_page.pack(side='left', padx=4)

        self.zoom_var = tk.DoubleVar(value=1.55)
        self.zoom_entry = ttk.Entry(self.top, textvariable=self.zoom_var, width=6)
        self.zoom_entry.pack(side='left', padx=4)
        ttk.Label(self.top, text='Zoom (x)').pack(side='left')

        self.btn_render = ttk.Button(self.top, text='렌더', command=self.render_page)
        self.btn_render.pack(side='left', padx=4)

        # '지우기' 버튼을 컬럼 콤보박스의 왼쪽으로 이동
        self.btn_clear = ttk.Button(self.top, text='지우기', command=self.clear_canvas)
        self.btn_clear.pack(side='left', padx=4)


        # Column selector (combo box) — values can be set via set_columns(columns)
        ttk.Label(self.top_option, text='컬럼:').pack(side='left', padx=4)
        df = self.load_csv()
        cols = list(df.columns)
        for col in cols:
            if ('.pdf' in col):
                cols.remove(col)
        self.col_combo = ttk.Combobox(self.top_option, values=cols, state='readonly', width=10)
        self.col_combo.pack(side='left', padx=4)

        # position label to show PDF coordinates when user clicks the canvas
        self.pos_var = tk.StringVar(value='')
        self.pos_label = ttk.Label(self.top_option, textvariable=self.pos_var)
        self.pos_label.pack(side='left', padx=4)

        # Column selector (combo box) — values can be set via set_columns(columns)
        ttk.Label(self.top_option, text='Font Size:').pack(side='left', padx=4)
        numbers = list(range(8, 21))
        self.size_combo = ttk.Combobox(self.top_option, values=numbers, state='readonly', width=3)
        self.size_combo.pack(side='left', padx=4)
        self.size_combo.set(12) 

        # Column selector (combo box) — values can be set via set_columns(makeoptions)
        ttk.Label(self.top_option, text='양식:').pack(side='left', padx=4)
        self.make_combo = ttk.Combobox(self.top_option, values=[], state='readonly', width=20)
        self.make_combo.pack(side='left', padx=4)

        self.btn_addmake = ttk.Button(self.top_option, text='Add', command=self.add_make_option)
        self.btn_addmake.pack(side='left', padx=4)

        # '지우기' 버튼을 컬럼 콤보박스의 왼쪽으로 이동
        self.btn_clearmake = ttk.Button(self.top_option, text='Clear', command=self.clear_make_option)
        self.btn_clearmake.pack(side='left', padx=4)

        # '미리보기' 버튼 추가
        self.btn_preview = ttk.Button(self.top_option, text='Preview', command=self.preview_option)
        self.btn_preview.pack(side='left', padx=4)

        # '양식 적용' 버튼 추가
        self.btn_apply = ttk.Button(self.top_option, text='Apply', command=self.apply_option)
        self.btn_apply.pack(side='left', padx=4)

        self.main = ttk.Frame(self.container)
        self.main.pack(fill='both', expand=True)

        self.canvas = tk.Canvas(self.main, bg='grey')
        self.hbar = ttk.Scrollbar(self.main, orient='horizontal', command=self.canvas.xview)
        self.vbar = ttk.Scrollbar(self.main, orient='vertical', command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
        self.canvas.grid(row=0, column=0, sticky='nsew')
        self.vbar.grid(row=0, column=1, sticky='ns')
        self.hbar.grid(row=1, column=0, sticky='ew')
        self.main.grid_rowconfigure(0, weight=1)
        self.main.grid_columnconfigure(0, weight=1)

        self.status_var = tk.StringVar(value='Ready')
        self.status = ttk.Label(self.container, textvariable=self.status_var)
        self.status.pack(fill='x')

        self.doc = None
        self.page = None
        self.pix_w = 0
        self.pix_h = 0
        self.page_rect = None
        self.tk_img = None
        self.img_id = None
        self.pdf_x = 0
        self.pdf_y = 0

        # bind click
        self.canvas.bind('<Button-1>', self.on_click)
        self.load_pdf()

    def load_csv(self, encoding=None):
        if pd is None:
            raise ImportError("pandas가 설치되어 있지 않습니다. 설치: pip install pandas")
        enc = encoding
        if enc is None:
            for e in ('utf-8', 'cp949', 'euc-kr'):
                try:
                    df = pd.read_csv(selected_csv_path, encoding=e)
                    return df
                except Exception:
                    pass
            raise ValueError("CSV 파일을 읽을 수 없습니다. 인코딩을 확인하세요.")
        return pd.read_csv(selected_csv_path, encoding=enc)

    def load_pdf(self):
        """Programmatically open a PDF file and update internal state. Calls on_pdf_selected callback if provided."""
        if fitz is None:
            messagebox.showerror('Error', 'PyMuPDF (fitz)가 설치되어 있지 않습니다. 설치: pip install pymupdf')
            return
        try:
            self.doc = fitz.open(selected_pdf_path)
        except Exception as e:
            messagebox.showerror('Error', f'PDF 열기 실패: {e}')
            return
        self.page_var.set(1)
        self.spin_page.config(to=max(1, self.doc.page_count))
        self.status_var.set(f'Opened: {os.path.basename(self.pdf_path)} Pages: {self.doc.page_count}')
        # notify parent/app about the selected PDF path
        if hasattr(self, 'on_pdf_selected') and callable(self.on_pdf_selected):
            try:
                self.on_pdf_selected(self.pdf_path)
            except Exception:
                pass
        # notify parent/app about the selected PDF path
        if hasattr(self, 'on_pdf_selected') and callable(self.on_pdf_selected):
            try:
                self.on_pdf_selected(self.pdf_path)
            except Exception:
                pass

    def render_page(self):
        if self.doc is None:
            messagebox.showwarning('경고', '먼저 PDF를 열어주세요.')
            return
        pnum = self.page_var.get()
        if pnum < 1 or pnum > self.doc.page_count:
            messagebox.showwarning('경고', f'올바른 페이지 번호를 입력하세요 (1-{self.doc.page_count}).')
            return
        try:
            zoom = float(self.zoom_var.get())
        except Exception:
            zoom = 2.0
            self.zoom_var.set(zoom)
        try:
            page = self.doc[pnum - 1]
            self.page = page
            self.page_rect = page.rect
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat, alpha=False)
            self.pix_w, self.pix_h = pix.width, pix.height

            if Image is None or ImageTk is None:
                messagebox.showerror('Error', 'Pillow가 설치되어 있지 않습니다. 설치: pip install pillow')
                return
            img = Image.frombytes('RGB', [pix.width, pix.height], pix.samples)
            self.tk_img = ImageTk.PhotoImage(img)

            self.canvas.delete('all')
            self.img_id = self.canvas.create_image(0, 0, anchor='nw', image=self.tk_img)
            self.canvas.config(scrollregion=(0, 0, self.pix_w, self.pix_h))
            self.status_var.set(f'Rendered page {pnum} ({self.pix_w}x{self.pix_h}) zoom {zoom}x')
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def clear_canvas(self):
        self.canvas.delete('all')
        self.page = None
        self.doc = None
        self.status_var.set('Cleared')
    
    def add_make_option(self):
        """Set the values for the make combo box."""
        try:
            if self.pos_var is None:
                messagebox.showwarning('경고', 'PDF 위치를 먼저 선택하세요.')

            option = "{0}:{1}={2}.{3}.{4}".format(str(self.page_var.get()), str(self.col_combo.get()), str(int(self.pdf_x)), str(int(self.pdf_y)), str(self.size_combo.get()))
            self.status_var.set(f'Added make option: {option}')
            if self.make_combo['values'] != []:
                current_values = list(self.make_combo['values'])
                if option not in current_values:
                    current_values.append(option)
                    self.make_combo['values'] = current_values
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def clear_make_option(self):
        """Clear the make combo box."""
        try:
            self.make_combo['values'] = []
            self.make_combo.set('')
        except Exception:
            pass

    def preview_option(self):
        """Clear the make combo box."""
        try:
        
            if self.make_combo['values'] == []:
                messagebox.showwarning('경고', '선택된 양식이 없습니다.')
                return
            else:
                current_values = list(self.make_combo['values'])

            # insert preview text on specified pages
            doc = fitz.open(selected_pdf_path)
            for v_text in current_values:
                p_text = v_text.split(':')
                page = doc[int(p_text[0])-1]
                page.insert_font("gulim", "C:\\Windows\\Fonts\\gulim.ttc")
                icols =  p_text[1].split('=')
                xy = icols[1].split('.')
                x = int(xy[0])
                y = int(xy[1])
                size = int(xy[2])
                intext = "미리보기_"+ str(icols[0])
                page.insert_text((x, y), intext, fontsize=size, fontname="gulim", color=(0.0, 0.0, 0.0))
            # persist the preview PDF temporarily
            out_pdf = selected_pdf_path.replace('.pdf', f'_preview.pdf')
            doc.save(out_pdf)
            os.startfile(out_pdf)
        except Exception as e:
                messagebox.showwarning('경고', str(e))

    def apply_option(self):
        """Clear the make combo box."""
        try:
        
            if self.make_combo['values'] == []:
                messagebox.showwarning('경고', '선택된 양식이 없습니다.')
                return
            else:
                current_values = list(self.make_combo['values'])
                makeList = ";".join(current_values)

            for e in ('utf-8', 'cp949', 'euc-kr'):
                try:
                    df = pd.read_csv(selected_csv_path, encoding=e)
                except Exception:
                    pass

            p_p = os.path.basename(selected_pdf_path)
            df[p_p] = makeList
            df.to_csv(selected_csv_path, index=False, encoding='utf-8-sig')
            self.root.destroy()

        except Exception as e:
                messagebox.showwarning('경고', str(e))
    
    def on_click(self, event):
        if self.page is None:
            return
        # canvas coords considering scroll
        cx = self.canvas.canvasx(event.x)
        cy = self.canvas.canvasy(event.y)
        # convert to PDF coordinates (points)
        rect = self.page_rect
        self.pdf_x = int(rect.x0 + (cx / self.pix_w) * rect.width)
        self.pdf_y = int(rect.y0 + (cy / self.pix_h) * rect.height)

        # update position label
        try:
            self.pos_var.set(f'PDF: x={self.pdf_x}, y={self.pdf_y}')
        except Exception:
            pass






