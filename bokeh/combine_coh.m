prefix = '/home/eric.coughlin/public_html/ER7/LineSearch/H1_COH_1116633616_1118275216_SHORT_1_webpage/data/';

files = dir([prefix '/*.mat']);
data = load([prefix '/' files(1).name]);
ff = data.freqs;

coherence_matrix = zeros(length(files), length(ff));
nfreqs = length(ff);
chnlnames = [];

for ii = 1:length(files)
    fprintf('%d / %d\n',ii,length(files));
    data = load([prefix '/' files(ii).name]);

    chnlname = strrep(files(ii).name,'.mat','');

    diff = length(ff) - length(data.coh);
    if diff
        extra = zeros(diff,1);
        temp_coh = [data.coh;extra];
    else
        temp_coh = data.coh;
    end
    coherence_matrix(ii,:) = temp_coh';
    chnlnames{ii} = chnlname;
   
end
save('coherence_1116633616_1118275216_SHORT_1.mat','ff','coherence_matrix','chnlnames','-v7.3');

