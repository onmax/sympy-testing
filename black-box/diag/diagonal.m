fileID = fopen('diagonals.txt','w');

v = [1 -1];
writeResults(fileID, v);

v = [2 1 -1 -2 -5];
writeResults(fileID, v);

fclose(fileID);



function writeResults(fileID, v)
fprintf(fileID, '%s\n', vector2mstr(v));
fprintf(fileID, '%s\n\n', matrix2mstr(diag(v)));
end
function vstr = vector2mstr(v)
    vstr = '[';
    for i=1:(size(v, 2))
        vstr = append(vstr, num2str(v(i)));
        if i ~= size(v,2)
            vstr = append(vstr, ',');
        end
    end
    vstr = append(vstr, ']');
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