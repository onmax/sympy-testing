fileID = fopen('ones.txt','w');

m = ones(5);
writeResults(fileID, m, "5,5");

m = ones(50);
writeResults(fileID, m, "50,50");

m = ones(4,7);
writeResults(fileID, m, "4,7");

m = ones(16, 1); 
writeResults(fileID, m, "16,1");

fclose(fileID);



function writeResults(fileID, m, t)
fprintf(fileID, '%s\n', t);
fprintf(fileID, '%s\n\n', matrix2mstr(m));
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