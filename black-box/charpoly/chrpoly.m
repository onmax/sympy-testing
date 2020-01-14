fileID = fopen('charpolies.txt','w');

m = [[1, -1, 3]; [3, 4, 2]; [0, 2, 5]];
writeResults(fileID, m);

m = [[1,2]; [3,4]];
writeResults(fileID, m);

m = [[2, 0]; [1, 3]];
writeResults(fileID, m);

m = [[-20, 10]; [10, -10]];
writeResults(fileID, m);

fclose(fileID);



function writeResults(fileID, m)
syms x
s = charpoly(m, x);
fprintf(fileID, '%s\n', matrix2mstr(m));
fprintf(fileID, '%s\n\n', s);
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