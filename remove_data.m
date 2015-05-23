
nodes = 1:500;
user = 'mcoughlin';

for i = 1:length(nodes)

   nodeDir = sprintf('/data/node%03d/%s',nodes(i),user);
   system_command = sprintf('rm -rf %s/*',nodeDir);

   system_command
   system(system_command)
end


