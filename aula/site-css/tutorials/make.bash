for i in *.rst; do rst2html --stylesheet=espai.css $i ./$i.html; done


#Coses velles
#----------------
#for i in *.rst; do rst2html --stylesheet=templatefull.css $i output_$i.html; done
#rst2odt --stylesheet=templatefullok.odt index.txt output.odt
#rst2html --stylesheet=templatefull.css index.txt output.html
