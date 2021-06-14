import streamlit as st
# import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

import seaborn as sns
# import datetime
# from tkinter import filedialog
import base64

# Title
st.sidebar.title('PJ-GROSS_PROFIT')
upload_file = st.sidebar.file_uploader(label = "",type = ['csv'])

def file_upload():
    if upload_file is not None:

        df = pd.read_csv(upload_file,encoding='shift-jis')
        csv_col_cnt = len(df.columns)

        if csv_col_cnt == 128:
        # if csv_col_cnt == 117:

            row_cnt_all = len(df)
            df_col = list(df.columns)
            
            st.markdown('### Extraction condition')
            st.markdown('` ` `抽出条件を指定` ` ` ')

            # wb_codeのlistを生成
            wb_code_ls = df.sort_values('wb_code')
            wb_code_ls = wb_code_ls['wb_code']
            wb_code_ls =wb_code_ls.drop_duplicates(keep='last')
            wb_code_ls = wb_code_ls.values.tolist()

            # ラジオボタン（wb_code）表示
            select_type = st.radio("Warehouse",('All', '[wb_code]'))
            if select_type == 'All':
                df2 = df[df['wb_code'].isin(wb_code_ls)]

            else:
                options = st.multiselect('Please select [wb_code]', wb_code_ls)
                df2 = df[df['wb_code'].isin(options)]
                df2 = df2.reset_index(drop=True)

            # c_codeのlistを生成
            c_code_ls = df2.sort_values('c_code')
            c_code_ls = c_code_ls['c_code']
            c_code_ls =c_code_ls.drop_duplicates(keep='last')
            c_code_ls = c_code_ls.values.tolist()

            # ラジオボタン（c_code）表示
            select_type2 = st.radio("User（Company）",('All', '[c_code]'))

            if select_type2 == 'All':
                df3 = df2[df2['c_code'].isin(c_code_ls)]
                df3 = df3.reset_index(drop=True)

            else:
                options2 = st.multiselect('Please select [c_code]', c_code_ls)
                df3 = df2[df2['c_code'].isin(options2)]
                df3 = df3.reset_index(drop=True)

            # channel_flgのlistを生成
            channel_flg_ls = df3.sort_values('channel_flg')
            channel_flg_ls = channel_flg_ls['channel_flg']
            channel_flg_ls = channel_flg_ls.drop_duplicates(keep='last')
            channel_flg_ls = channel_flg_ls.values.tolist()

            # ラジオボタン（channel_flg）表示
            select_type3 = st.radio("Channel",('All', '[channel_flg]'))

            if select_type3 == 'All':
                df8 = df3[df3['channel_flg'].isin(channel_flg_ls)]
                df8 = df8.reset_index(drop=True)

            else:
                options5 = st.multiselect('Please select [channel_flg]',
                [
                'Shopify',
                'stores',
                'Yahoo',
                'Ebay',
                'muzaiko',
                ]
                )
                
                df8 = df3[df3['channel_flg'].isin(options5)]
                df8 = df8.reset_index(drop=True)

            # ラジオボタン（strage_type）表示
            storage_type = st.radio(
                "Storage_type",
                ('All', 'specific', 'tsubo'))

            if storage_type == 'All':
                df9 = df8
            elif storage_type == 'specific':
                df9 = df8[df8['storage_type']=='specific']
            else :
                df9 = df8[df8['storage_type']=='tsubo']

            # 数値範囲指定を表示
            st.sidebar.markdown('### Numerical range')

            # 請求額（actual）
            st.sidebar.markdown('#### 1.請求額の範囲を指定') 
            actual_min = df9['actual'].min()
            actual_max = df9['actual'].max()

            xmin = st.sidebar.number_input('最小値（以上）：[actual]（単位：JPY）',actual_min, actual_max, actual_min)
            st.sidebar.write(actual_min)
            xmax = st.sidebar.number_input('最大値（以下）：[actual]（単位：JPY）',actual_min, actual_max, actual_max)
            st.sidebar.write(actual_max)

            df4 = df9[df9['actual'] <= xmax]
            df4 = df4[df4['actual'] >= xmin]
            df4 = df4.reset_index(drop=True)

            # 粗利率（profit_margin）
            st.sidebar.markdown('#### 2.粗利率の範囲を指定')
            profit_margin_min = df4['profit_margin'].min()
            profit_margin_max = df4['profit_margin'].max()

            xmin2 = st.sidebar.number_input('最小値（以上）：[profit_margin]（単位：%）',profit_margin_min, profit_margin_max, profit_margin_min)
            st.sidebar.write(profit_margin_min)
            xmax2 = st.sidebar.number_input('最大値（以下）：[profit_margin]（単位：%）',profit_margin_min, profit_margin_max, profit_margin_max)
            st.sidebar.write(profit_margin_max)

            df4 = df4[df4['profit_margin'] <= xmax2]
            df4 = df4[df4['profit_margin'] >= xmin2]
            df4 = df4.reset_index(drop=True)

            # カラム選択表示
            select_type3 = st.radio("Column",('All', 'Columns'))

            if select_type3 == 'All':
                df5 = df4
            else:
                options3 = st.multiselect(
                'Please select columns',
                df_col,
                [
                'target_term',
                'c_code',
                'wc_code',
                'wb_code',
                'actual',
                'retail',
                'wholesale',
                'profit',
                'profit_margin',
                'difference',
                'difference_margin'])
                df5 = df4[options3]

            st.markdown('### Extracted data')
            st.markdown('` ` `指定された条件で抽出された情報` ` ` ')

            st.dataframe(df5)

            row_cnt_select = len(df5)
            col_cnt = len(df5.columns)
            st.write(str(row_cnt_select) + '/' + str(row_cnt_all) + ' Records' + ' | ' + str(col_cnt) + ' Columns')

            # ダウンロードボタン
            download1 = st.button('Create as CSV file')
            if download1 == True:
                csv = df5.to_csv(index=False, encoding="shift-jis")
                b64 = base64.b64encode(csv.encode()).decode()  # some strings
                linko= f'<a href="data:file/csv;base64,{b64}" download="gross_profit_data_ex.csv">Download here</a>'
                st.markdown(linko, unsafe_allow_html=True)

            # ピポッドテーブル（縦持ち変換）
            st.markdown('### Pivot data')
            st.markdown('` ` `縦持ち変換した情報を表示` ` ` ')

            pivot = st.checkbox('Display on screen（dataframe）')
            if pivot == True:
                tate = df5.T
                st.dataframe(tate)

                # ダウンロードボタン
                download2 = st.button('Create as CSV file（Pivot）')
                if download2 == True:
                    if download2 == True:
                        csv = tate.to_csv(header=False, index=True, encoding="shift-jis")
                        b64 = base64.b64encode(csv.encode()).decode()  # some strings
                        linko= f'<a href="data:file/csv;base64,{b64}" download="gross_profit_data_pv.csv">Download here</a>'
                        st.markdown(linko, unsafe_allow_html=True)

            st.markdown('### Fundamental statistics')
            st.markdown('` ` `合計値を表示` ` ` ')
            df11 = pd.DataFrame(df4,columns=['actual','retail','wholesale','profit'])
            sum_df = df11.sum(axis = 0)
            st.dataframe(sum_df)

            st.markdown('` ` `基本統計量を表示` ` ` ')
            df6 = round(df4[['actual', 'retail', 'wholesale', 'profit', 'profit_margin']].describe())
            st.dataframe(df6)

            # 相関関係グラフの表示
            st.markdown('### Correlation')
            st.markdown('` ` `請求額[actual]と粗利率[profit_margin]の相関関係を表示` ` ` ')

            df7 = df4[['wc_code', 'actual', 'profit_margin', 'A_profit_margin',  'B_profit_margin', 'C_profit_margin', 'D_profit_margin', 'E_profit_margin', 'F_profit_margin']]
            df7['actual'] = round(df7['actual']/10000)

            graph = st.checkbox('Display on screen（graph）')
            if graph == True:

                options4 = st.multiselect(
                '',
                ['actual', 'profit_margin', 'A_profit_margin',  'B_profit_margin', 'C_profit_margin', 'D_profit_margin', 'E_profit_margin', 'F_profit_margin'],
                ['actual', 'profit_margin'])

                st.markdown('` ` `actual = 単位：JPY（万）` ` ` ')
                st.markdown('` ` `profit_margin = %` ` ` ')

                fig = sns.pairplot(df7, hue='wc_code',vars = options4)

                # x軸(xaxis)に対して、10ごと目盛りを入れる
                # ax = plt.gca()
                # ax.xaxis.set_major_locator(ticker.MultipleLocator(10))

                # グラフ表示
                st.pyplot(fig)

                df10 = df4[['target_term', 'channel_flg', 'actual', 'profit_margin']]
                df10['actual'] = round(df10['actual']/10000)

                fig2 = sns.catplot(x='target_term', y='actual', data=df10, kind='bar', hue='channel_flg', palette='Spectral')
                st.pyplot(fig2)

                fig3 = sns.catplot(x='target_term', y='profit_margin', data=df10, kind='bar', hue='channel_flg', palette='Spectral')
                st.pyplot(fig3)
                st.markdown('` ` `棒グラフ上に描かれる黒い線 = 95%信頼区間でのnerror barを示している。95%信頼区間とは、95%の確率で平均値がこの部分に含まれるという範囲のこと。` ` ` ')
        else:
             st.error('This file is not the specified csv file.')
    else:
        st.write('Please upload the specified file :sunglasses:')

file_upload()
