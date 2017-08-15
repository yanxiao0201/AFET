#!/bin/sh
Data='Acrobat'
Indir='Data/'$Data
Intermediate='Intermediate/'$Data
Outdir='Results/'$Data
bratdir='~/Documents/brat'
### Make intermediate and output dirs
mkdir -pv $Intermediate
mkdir -pv $Outdir

# echo 'Step 0 Generate Input from MetaMap output'
# echo 'TODO: brown'
# cd Metamap_to_AFET/
# python metamap_to_afet.py
# cd ..
# cp Metamap_to_AFET/AFET_input.json Data/$Data/train.json
# cp Metamap_to_AFET/AFET_input.json Data/$Data/test.json

# ### Generate features
# echo 'Step 1 Generate Features'
# python DataProcessor/feature_generation.py $Data 20 
# echo ' '

# ### Train AFET
# echo 'Step 2 Train AFET'
# Model/pl_warp $Data 50 0.01 50 10 0.15 0 1 1 5 1
# echo ' '

# ### Predict and evaluate
# echo 'Step 3 Predict and Evaluate'
# python Evaluation/emb_prediction.py $Data pl_warp bipartite maximum cosine 0.25
# python Evaluation/evaluation.py $Data pl_warp bipartite

# echo 'Step 4 Visualization'
# python visualization.py

echo 'Step 5 AFET to brat'
cp Acrobat_visualized_result.json AFET_to_brat/Acrobat_visualized_result.json
cd AFET_to_brat
python afet_result_only_to_brat.py
cd ..

echo 'Step 6 Evaluation'


for file in AFET_to_brat/AFET_to_brat/mapped_type/*.ann; 
	do cp $file $bratdir/data/AFET_result;
done



