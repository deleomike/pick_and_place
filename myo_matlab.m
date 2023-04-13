%% Set up the MiniVIE path
cd('C:\GitHub\MiniVIE');
MiniVIE.configurePath;

%% Create an object for UDP interface to the Myo Armband
hMyo = Inputs.MyoUdp.getInstance();
hMyo.initialize();

%% start up the signal viewer
hViewer = GUIs.guiSignalViewer(hMyo);

% come back to this folder
cd('C:\GitHub\hrilabs\Lab4_EMGControl');

cleanup;
cd('..\..\MiniVIE')
obj = MiniVIE;

% CHANGE THIS TO MATCH YOUR TRAINING DATA FILE
myDataFilename = 'C:\Users\HRIadmin\PycharmProjects\group1\kaufman_4_7_training.trainingData';
 
% Load training data file
hData = PatternRecognition.TrainingData();
hData.loadTrainingData(myDataFilename);
 
% Create EMG Myo Interface Object
hMyo = Inputs.MyoUdp.getInstance();
hMyo.initialize();
 
% Create LDA Classifier Object
hLda = SignalAnalysis.Lda;
hLda.initialize(hData);
hLda.train();
hLda.computeError();

counter = 0;
classes = [];

udpMyo = PnetClass(5007, 5006, '127.0.0.1');
udpMyo.enableLogging = true;
udpMyo.initialize();

StartStopForm([]); % initialize a small gui utility to control a while loop
while StartStopForm
        
    % Get the appropriate number of EMG samples for the 8 myo channels
    emgData = hMyo.getData(hLda.NumSamplesPerWindow,1:8);
    
    % Extract features and classify
    features2D = hLda.extractfeatures(emgData);
    [classDecision, voteDecision] = hLda.classify(reshape(features2D',[],1));
    
    % Display the resulting class number and name
    classes = [classes classDecision];
    counter = counter + 1;
    if counter == 5
        class = mode(classes);
        classNames = hLda.getClassNames;
        className = classNames{class};
        udpMyo.putData(uint8(class))
        fprintf('Class=%2d; Class = %16s;\n',class, className);
        counter = 0;
        classes = [];

    end

    % refresh the display
    drawnow;
 
end