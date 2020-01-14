fileID = fopen('cholesky.txt','w');

m22 = [[1, 0]; [0, 1]];
m33 = [[2, -1, 0]; [-1, 2, -1]; [0, -1, 2]];

writeResults(fileID, m22);
writeResults(fileID, m33);

fclose(fileID);



function writeResults(fileID, m)
r = chol(m);
fprintf(fileID, '%s\n', matrix2mstr(m));
fprintf(fileID, '%s\n\n', matrix2mstr(r));
end

function mstr = matrix2mstr(m)
mstr = '[';
for i=1:size(m, 1)
    mstr = append(mstr, '[');
    for j=1:(size(m, 2) - 1)
        mstr = append(mstr, num2str(m(i,j),15));
        mstr = append(mstr, ',');
    end
    mstr = append(mstr, num2str(m(i, size(m, 2)), 15));
    if i ~= size(m,1)
        mstr = append(mstr, '];');
    else
        mstr = append(mstr, ']');
    end
end
mstr = append(mstr, ']');
end             