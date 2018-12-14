# muon_project
Relevant Files and Python scripts for PHYS5011/5041 final project on the lifetime of muons.
*** CONDA OR MINICONDA IS REQUIRED ***
To install the "muon" conda environment from the xml (Essentially my personal setup):
  On a UNIX terminal, enter 'conda env create -f muon.xml'
  then 'source activate muon' to activate the environment
 
Unfortunately, rigolread.py can't be tested unless you have a RIGOL oscilloscope and a plastic scintillator detector. Though you could run a frequency generator through an oscilloscope to simulate it...

Some examples of the output of rigolread.py (data run files) are included in muonruns.zip. Though a small number of runs won't produce amazing results, it is great for testing code due to shorter computing time. Making sure everything is put in the same directory, run 'python3 Unpack.py' on your UNIX terminal. It will then ask for discriminator values (and give you a range suggestion) and create a txt file with decay times per value entered.

Now, you can either run 'python3 GenPlot.py' with the files you generated previously, or those included in decays.zip
While the generated files are good to test the self-consistency of the code, the provided files have many more runs associated to them.
*** DO NOT MIX THESE TWO IN THE SAME DIRECTORY, AS THE SCRIPT WILL TAKE BOTH TYPES AS INPUT AND BE INCONSISTENT ***
This is the final script, which will produce plots and output fit parameters.



