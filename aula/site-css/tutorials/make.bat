for %%x in (*.rst) do (
   c:\Python27\Scripts\rst2html.py %%x .\%%x.html --stylesheet=espai.css
)

move index.rst.html index.html
pause