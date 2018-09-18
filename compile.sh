#!/bin/sh
echo "compile_ae"
/nz/export/ae/utilities/bin/compile_ae --db $1 --language python \
     --version 3 --template deploy "./decision_tree.py" 
echo "copy whole current dir!"
export AE_PATH="/nz/export/ae/applications/$1/admin"
echo $AE_PATH
cp -R . $AE_PATH
echo "register_ae"
#/nz/export/ae/utilities/bin/register_ae --db $1 --language python --version 3 \
#    --template udtf --exe "./decision_tree.py" --sig "DT_TRAIN(VARARGS)" \
#    --return "TABLE(debug VARCHAR(255))" \
#    --level 2 \
#    --noparallel \
#    --environment "'NZAE_REGISTER_NZAE_HOST_ONLY_NZAE_PREPEND_LD_LIBRARY_PATH'='/nz/export/ae/applications/mypython/shared:/nz/export/ae/sysroot/spu/generic/x86_64-generic-linux-gnu/lib/:/nz/export/ae/languages/python/2.6/host/lib'" \
#    --environment "'NZAE_REGISTER_NZAE_SPU_ONLY_NZAE_PREPEND_LD_LIBRARY_PATH'='/nz/export/ae/applications/mypython/shared:/nz/export/ae/sysroot/spu/generic/x86_64-generic-linux-gnu/lib/:/nz/export/ae/languages/python/2.6/spu/lib'"

#trenowanie klasyfikatora
/nz/export/ae/utilities/bin/register_ae --db $1 --language python --version 3 \
    --template udtf --exe "./predict_from_tree.py" --sig "PUT_HT_PREDICT(VARARGS)" \
    --return "TABLE(debug VARCHAR(255))" \
    --level 2 \
    --rname put_ht \
    --noparallel \
    --environment "'NZAE_LOG_DIR'='/nz/export/ae/log'" \
    --environment "'NZAE_REGISTER_NZAE_HOST_ONLY_NZAE_PREPEND_LD_LIBRARY_PATH'='/nz/export/ae/applications/mypython/shared:/nz/export/ae/sysroot/spu/generic/x86_64-generic-linux-gnu/lib/:/nz/export/ae/languages/python/2.6/host/lib'" \
    --environment "'NZAE_REGISTER_NZAE_SPU_ONLY_NZAE_PREPEND_LD_LIBRARY_PATH'='/nz/export/ae/applications/mypython/shared:/nz/export/ae/sysroot/spu/generic/x86_64-generic-linux-gnu/lib/:/nz/export/ae/languages/python/2.6/spu/lib'"

#predykcja 
/nz/export/ae/utilities/bin/register_ae --db $1 --language python --version 3 \
    --template udtf --exe "./decision_tree.py" --sig "PUT_HT_TRAIN(VARARGS)" \
    --return "TABLE(debug VARCHAR(255))" \
    --level 2 \
    --rname put_ht \
    --noparallel \
    --environment "'NZAE_LOG_DIR'='/nz/export/ae/log'" \
    --environment "'NZAE_REGISTER_NZAE_HOST_ONLY_NZAE_PREPEND_LD_LIBRARY_PATH'='/nz/export/ae/applications/mypython/shared:/nz/export/ae/sysroot/spu/generic/x86_64-generic-linux-gnu/lib/:/nz/export/ae/languages/python/2.6/host/lib'" \
    --environment "'NZAE_REGISTER_NZAE_SPU_ONLY_NZAE_PREPEND_LD_LIBRARY_PATH'='/nz/export/ae/applications/mypython/shared:/nz/export/ae/sysroot/spu/generic/x86_64-generic-linux-gnu/lib/:/nz/export/ae/languages/python/2.6/spu/lib'"

#czyszczenie klasyfikatora
/nz/export/ae/utilities/bin/register_ae --db $1 --language python --version 3 \
    --template udtf --exe "./clean_model.py" --sig "PUT_HT_CLEAN(BOOL)" \
    --return "TABLE(state VARCHAR(255))" \
    --level 2 \
    --rname put_ht \
    --noparallel \
    --environment "'NZAE_LOG_DIR'='/nz/export/ae/log'" \
    --environment "'NZAE_REGISTER_NZAE_HOST_ONLY_NZAE_PREPEND_LD_LIBRARY_PATH'='/nz/export/ae/applications/mypython/shared:/nz/export/ae/sysroot/spu/generic/x86_64-generic-linux-gnu/lib/:/nz/export/ae/languages/python/2.6/host/lib'" \
    --environment "'NZAE_REGISTER_NZAE_SPU_ONLY_NZAE_PREPEND_LD_LIBRARY_PATH'='/nz/export/ae/applications/mypython/shared:/nz/export/ae/sysroot/spu/generic/x86_64-generic-linux-gnu/lib/:/nz/export/ae/languages/python/2.6/spu/lib'"

#select * from table with final(PUT_HT_LAUNCH(0));

#właczanie całego systemu
#/nz/export/ae/utilities/bin/register_ae --db $1 --language python --version 3 \
#    --template udtf --exe "./decision_tree.py" --sig "PUT_HT_LAUNCH(INT8)" \
#    --return "TABLE(aeresult varchar(255))" \
#    --level 2 \
#    --rname put_ht \
#    --launch \
#    --noparallel \
#    --environment "'NZAE_LOG_DIR'='/nz/export/ae/log'" \
#    --environment "'NZAE_REGISTER_NZAE_HOST_ONLY_NZAE_PREPEND_LD_LIBRARY_PATH'='/nz/export/ae/applications/mypython/shared:/nz/export/ae/sysroot/spu/generic/x86_64-generic-linux-gnu/lib/:/nz/export/ae/languages/python/2.6/host/lib'" \
#    --environment "'NZAE_REGISTER_NZAE_SPU_ONLY_NZAE_PREPEND_LD_LIBRARY_PATH'='/nz/export/ae/applications/mypython/shared:/nz/export/ae/sysroot/spu/generic/x86_64-generic-linux-gnu/lib/:/nz/export/ae/languages/python/2.6/spu/lib'"