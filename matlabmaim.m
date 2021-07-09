

%% crop

% Образка начального изображения, увеличение контраста, негативный снимок

crop = true;
inversion = false;
frame = [1; 1630; 201; 900];

for i = 1:numel(S)
    [S(i).fname] = CropInv(crop, inversion, frame, S, i, D, 1.3); % 1.3 - contrast
end
Done('Crop')
clear crop frame inversion D i

%% background

[S(1).res(1), S(1).res(2)] = size(imread(S(1).cropfname));
rawMin = 255 * uint8(ones(S(1).res(1), S(1).res(2)));
for i = 1:numel(S)
    [rawMin, S(i).res(1), S(i).res(2)] = Minimal(rawMin, S, i);
end
clear i
imwrite(rawMin, 'background.bmp')
Done('Background')

%% edge processing
se = strel('disk', 2);
for i = 1:numel(S)
    S(i).partparams = EdgeProcess(S, i, rawMin, se);
end
clear i se
Done('Edges')

%% Boxing and particles checking

for i = 1:numel(S)
    raw = imread(S(i).subsfilename);
    for j = 1:numel(S(i).partparams)
       [S(i).partparams(j).imagegrey, ...
           S(i).partparams(j).mmArea, ...
           S(i).partparams(j).mmEquivDiameter, ...
           S(i).partparams(j).check] = GreyCheck(raw, imdata, S, i, j);
    end
    S(i).particlesnumber = sum([S(i).partparams(:).check]);
end
clear i j raw
%%

nhdiv = 100;
nvdiv = 50;
d = (zeros(nhdiv, nvdiv));
[d,S] = Distribution(S, nvdiv, nhdiv, d);
clear nhdiv nvdiv
toc
%% plots
n = 12; % num of image to show
figure(1)
subplot(5,2,1)
imshow(imread(S(n).cropfname))
title('RAW crop image')
subplot(5,2,2)
imshow(rawMin)
title('Background (rawMin)')
subplot(5,2,3)
imshow(imread(S(n).subsfilename))
title('Substructed background')
% subplot(5,2,4)
figure()
imshow(S(n).thresholdfilename)
title('Threshold (I)')
% subplot(5,2,5)
figure()
imshow(S(n).edgefilename)
title('Edges of particles (E)')
% subplot(5,2,6)
figure()
imshow(imread(S(n).cropfname))
title('Centroids')
hold on
%%

 for i = 1:numel(S(n).partparams)
     x1 = uint16(S(n).partparams(i).BoundingBox(1));
     y1 = uint16(S(n).partparams(i).BoundingBox(2));
     x2 = x1 + uint16(S(n).partparams(i).BoundingBox(3)) - 1;
     y2 = y1 + uint16(S(n).partparams(i).BoundingBox(4)) - 1;
     plot([x1 x1 x2 x2 x1], [y1 y2 y2 y1 y1], 'w')
     if S(n).partparams(i).check
         plot(S(n).partparams(i).Centroid(1), S(n).partparams(i).Centroid(2), 'r+')
     else
         plot(S(n).partparams(i).Centroid(1), S(n).partparams(i).Centroid(2), 'r+')
     end
 end
clear x1 y1 x2 y2 i
%%
% subplot(5,2,9)
figure()
d1 = imgaussfilt(d,0.8)

imagesc(d)
imagesc(d1)
axis equal
figure()
contourf(d/391, 4)
axis ij
axis equal
figure()
contourf(d1/391, 4)
axis ij
axis equal

%%
close all
for i = 1:numel(S)
    raw = imread(S(i).cropfname);
    fig1488 = imshow(raw);

    hold on
    for j = 1:numel(S(i).partparams)
        plot(S(i).partparams(j).Centroid(1), S(i).partparams(j).Centroid(2), 'ro','LineWidth',2)
    end

    saveas(fig1488, S(i).detected, 'png')
    close all
    %pause(1)
end

%%
%  figure()
%  hold on
%  for i = 1:numel(S)
%      imshow(imread(S(i).fname))
%      hold on
%      for j = 1:numel(S(i).partparams)
%          plot(S(i).partparams(j).Centroid(1), S(i).partparams(j).Centroid(2), 'r+')
%      end
%      pause(0.02)
%      x1 = uint16(S(n).partparams(i).BoundingBox(1));
%      y1 = uint16(S(n).partparams(i).BoundingBox(2));
%      x2 = x1 + uint16(S(n).partparams(i).BoundingBox(3)) - 1;
%      y2 = y1 + uint16(S(n).partparams(i).BoundingBox(4)) - 1;
%      plot([x1 x1 x2 x2 x1],[y1 y2 y2 y1 y1])
%      plot(S(n).partparams(i).Centroid(1), S(n).partparams(i).Centroid(2), 'r+')
%  end
%  clear x1 x2 y1 y2
%  clear i
%  %%
%  for k = 1:numel(S)-1
%      for i = 1:numel(S(k).partparams)
%          if S(k).partparams(i).check
%              jmax = 0;
%              pmax = 0;
%              for j = 1:numel(S(k+1).partparams)
%                  dx = S(k).partparams(i).Centroid(1) - S(k+1).partparams(j).Centroid(1); %+ 16;
%                  dy = S(k).partparams(i).Centroid(2) - S(k+1).partparams(j).Centroid(2) + 16;
%                  R = sqrt(dy*dy + dx*dx);
%                  if R < 30
%                      R= 1-R/30;
%                  else
%                      R = NaN;
%                  end
%                  A = abs(S(k).partparams(i).Area/S(k+1).partparams(j).Area - 1);
%                  if A < 0.3
%                      A = 1-A/0.3;
%                  else
%                      A = NaN;
%                  end
%
%                  C = abs(S(k).partparams(i).Circularity/S(k+1).partparams(j).Circularity - 1);
%                  if C < 0.3
%                      C = 1 - C/0.3;
%                  else
%                      C = NaN;
%                  end
%                  B = (A + R + C);
%                  if pmax < B
%                      pmax = B;
%                      jmax = j;
%                  end
%              end
%               S(k).partparams(i).pair = jmax;
%          end
%      end
%  end
%
% clear A B C d dx dy f g i j k t R
% toc
%
% for o = 1:100
%     for i = 1:numel(S)-1
%         imshow(imread(S(i).fname))
%         hold on
%         for j = 1:numel(S(i).partparams)
%             if ~isnan(S(i).partparams(j).pair)
%             plot(S(i).partparams(j).Centroid(1), S(i).partparams(j).Centroid(2),'r+')
%             plot([S(i).partparams(j).Centroid(1), ...
%                 S(i+1).partparams((S(i).partparams(j).pair)).Centroid(1)],       ...
%                 [S(i).partparams(j).Centroid(2), ...
%                 S(i+1).partparams((S(i).partparams(j).pair)).Centroid(2)])
%             end
%         end
%         pause(0.02)
%
%     end
%
% end
