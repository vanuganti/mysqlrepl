# Rakefile

# what's the name of this project
PROJECT_NAME = 'mysqlrepl'

desc "build & start containers in foreground"
task :run do
    run_command "docker-compose -p #{PROJECT_NAME} up"
end

desc 'start the containers in background and seed demo data'
task :demo => [:restart,:test] do
end

desc 'start the containers in background'
task :start do
    run_command "docker-compose -p #{PROJECT_NAME} up -d"
    print "containers status"
    run_command "docker ps -a | grep #{PROJECT_NAME}"
end

desc "stop and remove all services"
task :stop do
    run_command "docker-compose -p #{PROJECT_NAME} stop"
    run_command "docker-compose -p #{PROJECT_NAME} rm -f"
end

desc "build the containers"
task :build do
    run_command "docker-compose -p #{PROJECT_NAME} build"
end

desc "get the status of containers"
task :status do
    run_command "docker ps -f name=#{PROJECT_NAME} -n=5"
end

desc "initialize containers"
task :init do
    print 'Creating necessary user accounts'
    run_command "docker exec -it #{PROJECT_NAME}_mysql1_1 /usr/bin/mysql -e \"grant all on *.* to 'mysql'@'%' identified by 'mysql'; set global auto_increment_offset=1; set global auto_increment_increment=4;\""
    run_command "docker exec -it #{PROJECT_NAME}_mysql2_1 /usr/bin/mysql -e \"grant all on *.* to 'mysql'@'%' identified by 'mysql'; set global auto_increment_offset=2; set global auto_increment_increment=4;\""
    run_command "docker exec -it #{PROJECT_NAME}_mysql3_1 /usr/bin/mysql -e \"grant all on *.* to 'mysql'@'%' identified by 'mysql'; set global auto_increment_offset=3; set global auto_increment_increment=4;\""
    run_command "docker exec -it #{PROJECT_NAME}_mysql4_1 /usr/bin/mysql -e \"grant all on *.* to 'mysql'@'%' identified by 'mysql'; set global auto_increment_offset=4; set global auto_increment_increment=4;\""
    run_command "docker exec -it #{PROJECT_NAME}_mysql5_1 /usr/bin/mysql -e \"grant all on *.* to 'mysql'@'%' identified by 'mysql'; set global auto_increment_offset=5; set global auto_increment_increment=4;\""
end

desc 'initialize all mysql services and test the replication'
task :test => [:init] do
    run_command "python test.py"
    puts "Checking the records in main shard (should be multiples of all shards)"
    run_command "docker exec -it #{PROJECT_NAME}_mysql5_1 /usr/bin/mysql -v -v -e \"select count(*) from shardm.test\""
end

desc 'start the containers in background and seed demo data'
task :restart => [:stop,:start] do
end

def run_command(command)
    puts command
    system(command) or raise("unable to execute command - #{command}")
end

def print(command)
    puts
    puts "-------------------------------------------"
    puts command
    puts "-------------------------------------------"
end
