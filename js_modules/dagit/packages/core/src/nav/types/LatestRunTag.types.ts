// Generated GraphQL types, do not edit manually.

import * as Types from '../../graphql/types';

export type LatestRunTagQueryVariables = Types.Exact<{
  runsFilter?: Types.InputMaybe<Types.RunsFilter>;
}>;

export type LatestRunTagQuery = {
  __typename: 'DagitQuery';
  pipelineRunsOrError:
    | {__typename: 'InvalidPipelineRunsFilterError'}
    | {__typename: 'PythonError'}
    | {
        __typename: 'Runs';
        results: Array<{
          __typename: 'Run';
          id: string;
          status: Types.RunStatus;
          runId: string;
          startTime: number | null;
          endTime: number | null;
          updateTime: number | null;
        }>;
      };
};
