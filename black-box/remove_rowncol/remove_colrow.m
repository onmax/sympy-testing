fileID = fopen('colrow.txt','w');

m = [[1, -1, 3]; [3, 4, 2]; [0, 2, 5]];
writeResults(fileID, m, 2, 2);

m = [[1,2]; [3,4]];
writeResults(fileID, m, 1, 1);

m = [[2, 0]; [1, 3]];
writeResults(fileID, m, 2, 1);

fclose(fileID);



function writeResults(fileID, m, r, c)
mc = m;
mc(r,:) = [];
mc(:,c) = [];
fprintf(fileID, '%s\n', matrix2mstr(m));
fprintf(fileID, '(%d,%d)\n', [r,c]);
fprintf(fileID, '%s\n\n', matrix2mstr(mc));
end

function mstr = matrix2mstr(m)
mstr = '[';
for i=1:size(m, 1)
    mstr = append(mstr, '[');
    for j=1:(size(m, 2) - 1)
        mstr = append(mstr, num2str(m(i,j)));
        mstr = append(mstr, ',');
    end
    mstr = append(mstr, num2str(m(i, size(m, 2))));
    if i ~= size(m,1)
        mstr = append(mstr, '];');
    else
        mstr = append(mstr, ']');
    end
end
mstr = append(mstr, ']');
end