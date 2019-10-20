#!/usr/bin/env bash

ROOT=$(dirname $0)
OUT=eumak.py

cp ${ROOT}/_eumak.py ${OUT}
echo '' >> ${OUT}
echo '' >> ${OUT}
echo 'DATA = """\' >> ${OUT}
base64 ${ROOT}/xkb/symbols/eumak >> ${OUT}
echo '"""' >> ${OUT}
echo '' >> ${OUT}
echo '' >> ${OUT}
echo 'if __name__ == "__main__":' >> ${OUT}
echo '    main()' >> ${OUT}
