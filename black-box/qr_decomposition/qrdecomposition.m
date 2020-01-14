fileID = fopen('qr.txt','w');

m22 = [[1, 2]; [3, 4]];
m33 = [[1, -1, 3]; [3, 4, 2]; [0, 2, 5]];
m44 = [[2,  -1, 1, 8]; [11, 4, 2, 0]; [9, 8, 5, 9]; [12,  -7,  -1, 6]];

writeResults(fileID, m22);
writeResults(fileID, m33);
writeResults(fileID, m44);

fclose(fileID);



function writeResults(fileID, m)
[Q,R] = qr(m);
fprintf(fileID, '%s\n', matrix2mstr(m));
fprintf(fileID, '%s\n', matrix2mstr(abs(Q)));
fprintf(fileID, '%s\n\n', matrix2mstr(abs(R)));
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