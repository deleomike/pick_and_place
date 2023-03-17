% MDL_CYTON Create model of the Cyton Gamma 300
%
% MDL_CYTON is a script that creates the workspace variable cyton which
% describes the kinematic and dynamic characteristics of a Robai Cyton
% Gamma 300 manipulator using standard DH conventions. 
%
% Also define the workspace vectors:
%   qz         zero joint angle configuration
%   qr         vertical 'READY' configuration
%   qstretch   arm is stretched out in the X direction
%   qn         arm is at a nominal non-singular configuration
%
% Notes::
% - SI units are used.
%
% Reference::
% - "A search for consensus among model parameters reported for the PUMA 560 robot",
%   P. Corke and B. Armstrong-Helouvry, 
%   Proc. IEEE Int. Conf. Robotics and Automation, (San Diego), 
%   pp. 1608-1613, May 1994.
%
% See also SerialRevolute, mdl_puma560akb, mdl_stanford.

clear L

deg = pi/180;

elbow_rotate = 105;
shoulder_lim = [-150 150]*deg;
elbow_lim = [-elbow_rotate elbow_rotate]*deg;

% Base Joint
L(1) = Revolute( ...
    'd', 0.120, ...
    'a', 0, ...
    'alpha', pi/2, ...
    'qlim', shoulder_lim);

L(2) = Revolute( ...
    'd', 0, ...
    'a', 0.1408, ...
    'alpha', -pi/2, ...
    'qlim', elbow_lim, ...
    'offset',pi/2);

L(3) = Revolute( ...
    'd', 0, ...
    'a', .0718, ...
    'alpha', -pi/2, ...
    'qlim', elbow_lim);

L(4) = Revolute( ...
    'd', 0, ...
    'a', .0718, ...
    'alpha', pi/2, ...
    'qlim', elbow_lim);

L(5) = Revolute( ...
    'd', 0, ...
    'a', .1296, ...
    'alpha', pi/2, ...
    'qlim', elbow_lim);

L(6) = Revolute('alpha', -pi/2);


qz = [0 0 0 0 0 0]; % zero angles, L shaped pose
qr = [0 pi/2 -pi/2 0 0 0]; % ready pose, arm up
qs = [0 0 -pi/2 0 0 0];
qn=[0 pi/4 pi 0 pi/4  0];


cyton = SerialLink(L, ...
    'name', 'Robai Cyton', ...
    'configs', {'qz', qz, 'qr', qr, 'qs', qs, 'qn', qn});


clear L