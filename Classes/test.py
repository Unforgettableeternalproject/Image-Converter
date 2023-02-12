self.promptL["text"] = "test"
self.promptU["text"] = "導入網路檔案"
self.btnU["text"] = "..."
self.promptC["text"] = "或者...從雲端導入"
self.sva.set('network status: {}'.format("online" if self.status else "offline"))
self.label["text"] = "浮水印預定放置區塊"
self.color_block_label["text"] = "遮罩顏色預覽:"
self.color_block_btn["text"] = "疊加"
self.color_block_btn2["text"] = "撤銷"
self.H_label["text"] = "色相:"
self.S_label["text"] = "飽和度:"
self.V_label["text"] = "明度:"
self.erodebtn["text"] = "侵蝕++"
self.dilatebtn["text"] = "膨脹++"
self.eddisplay["text"] = "平衡落差:"
self.openingck["text"] = "去白點"
self.closingck["text"] = "去黑點"
self.gradientck["text"] = "只顯示輪廓"
self.clabel["text"] = "其他效果:"
self.clist["value"] = ["無", "中值降噪", "高斯模糊", "銳利化", "自適應二值化", "灰階"]
self.c_confirm["text"] = "應用" 
self.distext["text"] = "原始圖片尺寸:"
self.display["text"] = "尚未導入!!"
self.fixedscale["text"] = "固定圖片比例"
self.zlabel["text"] = "縮放(?):"
self.tp = Hovertip(self.zlabel,'當固定比例被開啟時才可用')
self.relabel["text"] = "自訂尺寸:"
self.s_confirm["text"] = "設定尺寸"
self.rolabel["text"] = "翻轉:"
self.n_flipbtn["text"] ="不翻轉"
self.h_flipbtn["text"] = "水平翻轉"
self.v_flipbtn["text"] = "垂直翻轉"
self.b_flipbtn["text"] = "水平+垂直"
self.crolabel["text"] = "旋轉:"
self.degree["text"] = "度"
self.dlist["value"] = ["順時針", "逆時針"]
self.d_confirm["text"] = "設定旋轉"
self.idlabel["text"] = "圖片資訊:"
self.imgnamedis["text"] = "檔案名稱:"
self.imgname["text"] = "尚未導入!!"
self.impwaydis["text"] = "導入方式:"
self.impway["text"] = "尚未導入!!"
self.undo["text"] = "還原上一動作"
self.redo["text"] = "重作上一動作"
self.plabel["text"] = "預覽圖片:"
self.promptE["text"] = "導出檔案"
self.localS["text"] = "儲存至電腦"
self.cloudS["text"] = "上傳至雲端(?)"
self.tp2 = Hovertip(self.cloudS, "目前只支援Google雲端硬碟")
self.mails["text"] = "寄送給他人"

#菜單
self.menu = tk.Menu()

self.win.config(menu=self.menu)
self.file.delete('顯示範例')
self.file.delete('完全重置')
self.file.add_command(label='Show example', command=self.example) #程式中顯示範例圖片檔的預覽
self.file.add_command(label='RESET ALL', foreground='red', command=self.resetall) #跳出視窗顯示警告，並詢問是否真的要重置

self.window.delete('步驟紀錄')
self.window.delete('開發者資訊')
self.window.add_command(label='Step record') #跳出新視窗，顯示步驟紀錄
self.window.add_command(label ='Developer info') #跳出新視窗，顯示開發者資訊

self.view_options.delete('小')
self.view_options.delete('中等')
self.view_options.delete('大')
self.view.delete('更改視窗大小')
self.view_options.add_command(label='Small') #變更為小視窗
self.view_options.add_command(label='Medium') #變更為中等視窗
self.view_options.add_command(label='Large') #變更為大視窗
self.view.add_cascade(label='Change window size', menu=self.view_options) #給予更改視窗比例的選項

self.window.delete('功能介紹')
self.help.delete('聯絡開發者')
self.window.add_command(label='Help') #跳出新視窗，顯示一個功能介紹的畫面(Help)
self.help.add_command(label='Contact') #跳出新視窗，內嵌開發者聯絡資訊(直接寄信?)

self.menu.delete('檔案')
self.menu.delete('視窗')
self.menu.delete('顯示')
self.menu.delete('幫助')
self.menu.add_cascade(label='File', menu=self.file)
self.menu.add_cascade(label='Window', menu=self.window)
self.menu.add_cascade(label='View', menu=self.view)
self.menu.add_cascade(label='Help', menu=self.help)