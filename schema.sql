create table
  public.chore (
    id bigint generated by default as identity not null,
    name text null,
    location_in_house text null,
    frequency text null,
    duration_mins bigint null default '0'::bigint,
    constraint chore_pkey primary key (id)
  ) tablespace pg_default;

create table
  public.roommate (
    id bigint generated by default as identity not null,
    first_name text null,
    last_name text null,
    email text null,
    constraint roommate_pkey primary key (id)
  ) tablespace pg_default;

create table
  public.chore_assignment (
    id bigint generated by default as identity not null,
    chore_id bigint null,
    roommate_id bigint null,
    status text null,
    constraint chore_assignment_pkey primary key (id),
    constraint chore_assignment_chore_id_fkey foreign key (chore_id) references chore (id),
    constraint chore_assignment_roommate_id_fkey foreign key (roommate_id) references roommate (id)
  ) tablespace pg_default;

create table
  public.bill_list (
    id bigint generated by default as identity not null,
    bill_id bigint null,
    roommate_id bigint null,
    status text null,
    constraint bill_list_pkey primary key (id),
    constraint bill_list_bill_id_fkey foreign key (bill_id) references bill (id)
  ) tablespace pg_default;

create table
  public.bill (
    id bigint generated by default as identity not null,
    cost double precision null,
    due_date timestamp with time zone null default (now() at time zone 'utc'::text),
    bill_type text null,
    message text null,
    constraint bill_pkey primary key (id)
  ) tablespace pg_default;